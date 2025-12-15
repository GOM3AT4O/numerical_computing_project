<h1 align="center">Numerical Computing Project</h1>

<p align="center">A full-stack application for numerical analysis</p>

<div align="center">
    <a href="https://github.com/TarekSaeed0/numerical_computing_project/pulse">
        <img alt="last commit" src="https://img.shields.io/github/last-commit/TarekSaeed0/numerical_computing_project?style=for-the-badge&labelColor=%231e1e2e&color=%2394e2d5">
    </a>
    <a href="https://github.com/TarekSaeed0/numerical_computing_project/stargazers">
        <img alt="Repo stars" src="https://img.shields.io/github/stars/TarekSaeed0/numerical_computing_project?style=for-the-badge&labelColor=%231e1e2e&color=%23f9e2af">
    </a>
    <a href="https://github.com/TarekSaeed0/numerical_computing_project">
        <img alt="Repo size" src="https://img.shields.io/github/repo-size/TarekSaeed0/numerical_computing_project?style=for-the-badge&labelColor=%231e1e2e&color=%2374c7ec">
    </a>
</div>

## Features

- Solving systems of simultaneous linear equations
- Solving non-linear equations
- Various numerical methods to use and compare
- Setting a precision for the calculations to be done in
- Step by step solution

## Download

|![Windows](https://img.shields.io/badge/Windows-0078D4?logo=windows&logoColor=white&style=for-the-badge)|![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white&style=for-the-badge)|![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black&style=for-the-badge)|
|---|---|---|
|[Download](https://github.com/TarekSaeed0/numerical_computing_project/releases/download/numerical_computing_project-v0.1.0/numerical_computing_project_0.1.0_x64_en-US.msi)|[Download](https://github.com/TarekSaeed0/numerical_computing_project/releases/download/numerical_computing_project-v0.1.0/numerical_computing_project_0.1.0_aarch64.dmg)|[Download](https://github.com/TarekSaeed0/numerical_computing_project/releases/download/numerical_computing_project-v0.1.0/numerical_computing_project_0.1.0_amd64.deb)|

See [releases](https://github.com/TarekSaeed0/numerical_computing_project/releases) for all available installers

## Build

### Dependencies

- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Node.js](https://nodejs.org/en/download)
- [Rust](https://rust-lang.org/tools/install/)
- [Tauri](https://v2.tauri.app/start/prerequisites/)

Run the following to create a virtual environment:

```sh
python -m venv venv
```

Then, activate the environment, depending on your shell the command differs, but for example, in Bash:

```bash
source venv/bin/activate
```

and in Powershell:

```ps1
PS C:\> venv\Scripts\Activate.ps1
```

Install the dependencies for the backend:

```sh
pip install -r backend/requirements.txt
```

Finally, build the Tauri applications

```sh
cd frontend
npm run tauri build
```
