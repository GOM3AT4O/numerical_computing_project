use std::{path::Path, process::Command};

fn main() {
    println!("cargo:rerun-if-changed=../../backend/app.py");
    println!("cargo:rerun-if-changed=../../backend/");

    let status = Command::new("pyinstaller")
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

    let target_triple = std::env::var("TARGET").expect("TARGET environment variable not set");

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
