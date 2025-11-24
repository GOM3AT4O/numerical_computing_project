use std::{
    process::{Command, Stdio},
    sync::{Arc, Mutex},
};

use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let child = Command::new("python")
                .args(["../../backend/app.py"])
                .stdout(Stdio::inherit())
                .stderr(Stdio::inherit())
                .spawn()
                .expect("error starting python backend");

            let child = Arc::new(Mutex::new(Some(child)));

            let child_clone = Arc::clone(&child);

            app.get_webview_window("main")
                .unwrap()
                .on_window_event(move |event| {
                    if let tauri::WindowEvent::CloseRequested { .. } = event {
                        if let Ok(mut child) = child_clone.lock() {
                            if let Some(mut child) = child.take() {
                                let _ = child.kill();
                                let _ = child.wait();
                            }
                        }
                    }
                });

            Ok(())
        })
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
