use std::{path::Path, process::Command};

fn main() {
    println!("cargo:rerun-if-changed=../../backend/app.py");
    println!("cargo:rerun-if-changed=../../backend/");

    let status = Command::new("../../backend/venv/bin/pyinstaller")
        .args([
            "--onefile",
            "--distpath",
            "../sidecars",
            "--workpath",
            "../backend-build",
            "--specpath",
            "../backend-build",
            "--name",
            "backend",
            "../../backend/app.py",
        ])
        .status()
        .expect("error running PyInstaller");

    if !status.success() {
        panic!("PyInstaller build failed");
    }

    let output = Command::new("rustc")
        .arg("-vV")
        .output()
        .expect("failed to run rustc -vV");
    let stdout = String::from_utf8_lossy(&output.stdout);
    let target_triple = stdout
        .lines()
        .find_map(|line| line.strip_prefix("host: "))
        .expect("failed to find host triple in rustc -vV output");

    let extension = if cfg!(target_os = "windows") {
        ".exe"
    } else {
        ""
    };

    let src = Path::new("../sidecars").join(format!("backend{}", extension));
    let dest = Path::new("../sidecars").join(format!("backend-{}{}", target_triple, extension));

    std::fs::rename(&src, &dest)
        .unwrap_or_else(|_| panic!("Failed to rename {:?} to {:?}", src, dest));

    tauri_build::build()
}
