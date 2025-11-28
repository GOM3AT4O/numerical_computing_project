use tauri_plugin_shell::process::CommandEvent;

use tauri::RunEvent;

use tauri_plugin_http::reqwest;
use tauri_plugin_shell::ShellExt;
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_http::init())
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let app_handle = app.handle();

            let (mut rx, _child) = app_handle
                .shell()
                .sidecar("backend")
                .expect("failed to create sidecar command")
                .spawn()
                .expect("failed to spawn sidecar process");

            tauri::async_runtime::spawn(async move {
                while let Some(event) = rx.recv().await {
                    match event {
                        CommandEvent::Stdout(line_bytes) => {
                            let line = String::from_utf8_lossy(&line_bytes);
                            println!("[backend stdout] {}", line);
                        }
                        CommandEvent::Stderr(line_bytes) => {
                            let line = String::from_utf8_lossy(&line_bytes);
                            eprintln!("[backend stderr] {}", line);
                        }
                        _ => {}
                    }
                }
            });

            println!("[tauri] sidecar started");

            Ok(())
        })
        .plugin(tauri_plugin_opener::init())
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|_app_handle, event| {
            if let RunEvent::ExitRequested { .. } = event {
                reqwest::blocking::Client::new()
                    .post("http://127.0.0.1:5000/shutdown")
                    .send()
                    .ok();

                println!("[tauri] sidecar closed.");
            }
        });
}
