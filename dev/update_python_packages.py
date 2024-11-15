# Copyright (c) 2024 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import pathlib
import subprocess
import tempfile
import zipfile


def main():
    python_dist_dir = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "Vendors",
        )
    )

    requirements_txt = os.path.join(python_dist_dir, "requirements.txt")

    frozen_requirements_txt = os.path.join(
        python_dist_dir,
        "frozen_requirements.txt",
    )

    pkgs_zip_path = os.path.join(python_dist_dir, "pkgs.zip")

    if not os.path.exists(requirements_txt):
        raise Exception(f"Cannot find requirements file {requirements_txt}")

    with tempfile.TemporaryDirectory() as temp_dir:
        print("Installing common Python packages...")

        temp_dir_path = pathlib.Path(temp_dir)

        # Pip install everything and capture everything that was installed.
        subprocess.run(
            [
                "python",
                "-m",
                "pip",
                "install",
                "--requirement",
                requirements_txt,
                "--no-compile",
                # The combination of --target and --upgrade forces pip to install
                # all packages to the temporary directory, even if an already existing
                # version is installed
                "--target",
                temp_dir,
                "--upgrade",
            ]
        )
        subprocess.run(
            ["python", "-m", "pip", "freeze", "--path", temp_dir],
            stdout=open(frozen_requirements_txt, "w"),
        )

        # Quickly compute the number of requirements we have.
        nb_dependencies = len([_ for _ in open(frozen_requirements_txt, "rt")])

        # Figure out if those packages were installed as single file packages or folders.
        package_names = [
            package_name
            for package_name in os.listdir(temp_dir)
            if "info" not in package_name and package_name != "bin"
        ]

        # Make sure we found as many Python packages as there
        # are packages listed inside frozen_requirements.txt
        # assert len(package_names) == nb_dependencies
        assert len(package_names) >= nb_dependencies

        # Write out the zip file for python packages. Compress the zip file with ZIP_DEFLATED. Note
        # that this requires zlib to decompress when importing.
        pkgs_zip = zipfile.ZipFile(pkgs_zip_path, "w", zipfile.ZIP_DEFLATED)

        for package_name in package_names:
            print(f"Zipping {package_name}...")

            full_package_path = temp_dir_path / package_name

            # If we have a .py file to zip, simple write it
            # full_package_path = temp_dir_path / package_name
            if full_package_path.suffix == ".py":
                pkgs_zip.write(
                    full_package_path, full_package_path.relative_to(temp_dir)
                )
            else:
                # Otherwise zip package folders recursively.
                zip_recursively(pkgs_zip, temp_dir_path, package_name)

        for filename in os.listdir(temp_dir):
            if not filename.endswith("-info"):
                continue
            if not os.path.isdir(os.path.join(temp_dir, filename)):
                continue

            zip_recursively(pkgs_zip, temp_dir_path, filename)


def zip_recursively(zip_file, root_dir, folder_name):
    """Zip the files at the given folder recursively."""

    for root, _, files in os.walk(root_dir / folder_name):
        for f in files:
            full_file_path = pathlib.Path(os.path.join(root, f))
            zip_file.write(full_file_path, full_file_path.relative_to(root_dir))


if __name__ == "__main__":
    main()
