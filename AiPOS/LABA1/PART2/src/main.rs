use std::io::{self, BufRead, Write, Read};
use std::net::{TcpStream, Shutdown};
use std::str;
use std::fs::{OpenOptions};
use std::time::SystemTime;
use chrono::{Local, Datelike, Timelike};

const DEFAULT_FILENAME: &str = "log.txt";

fn write_to_file(content: &str) -> io::Result<()> {
    let current_time = SystemTime::now();
    let local_time: chrono::DateTime<Local> = current_time.into();

    let year = local_time.year();
    let month = local_time.month();
    let day = local_time.day();
    let hour = local_time.hour();
    let minute = local_time.minute();
    let second = local_time.second();

    let time_str = format!("{}-{:02}-{:02} {:02}:{:02}:{:02}", year, month, day, hour, minute, second);
    let line = format!("{}\t{}\n", time_str, content);

    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(DEFAULT_FILENAME)?;

    file.write_all(line.as_bytes())?;

    Ok(())
}
fn main() -> io::Result<()> {
    println!("TCP DEMO CLIENT");

    let mut current_server_addr: Option<String> = None;
    let mut current_port: Option<u16> = None;
    let mut stream: Option<TcpStream> = None;

    'main_loop: loop {
        let stdin = io::stdin();
        let mut reader = stdin.lock();
        let mut buffer = String::new();

        loop {
            print!("Connect to server. Use 'connect <address> <port>' or 'quit' to exit. \n");
            io::stdout().flush()?;
            reader.read_line(&mut buffer)?;

            if buffer.trim() == "quit" {
                println!("Exit...");
                if let Some(s) = stream.take() {
                    s.shutdown(Shutdown::Both)?;
                }
                return Ok(());
            } else if buffer.starts_with("disconnect") {
                println!("You are not connected.");
            } else if buffer.starts_with("connect") {
                let parts: Vec<&str> = buffer.split_whitespace().collect();
                if parts.len() != 3 {
                    println!("Invalid command format. Use 'connect <address> <port>'.");
                } else {
                    let new_server_addr = parts[1].to_string();
                    let new_port = parts[2].parse::<u16>();
                    match new_port {
                        Ok(port) => {
                            current_server_addr = Some(new_server_addr.clone());
                            current_port = Some(port);
                            println!("Connection to {}:{}...", new_server_addr, port);

                            if let Some(s) = stream.take() {
                                s.shutdown(Shutdown::Both)?;
                            }

                            match TcpStream::connect((new_server_addr.as_str(), port)) {
                                Ok(s) => {
                                    stream = Some(s);

                                    let line = format!("CONNECTED to {}:{}",
                                                       new_server_addr,
                                                       port);
                                    match write_to_file(line.as_str()) {
                                        Ok(_) => {},
                                        Err(e) => eprintln!("Error writing to file: {}", e),
                                    }
                                }
                                Err(e) => {
                                    eprintln!("Connection error: {}", e);
                                    stream = None;
                                }
                            }
                            buffer.clear();
                            break;
                        }
                        Err(_) => {
                            println!("Invalid port format. Use 'connect <address> <port>'.");
                        }
                    }
                }
            } else {
                println!("You must first connect with 'connect <address> <port>'.");
            }

            buffer.clear();
        }

        if let Some(s) = stream.as_mut() {
            loop {
                reader.read_line(&mut buffer)?;

                if buffer.trim() == "quit" {
                    println!("Exit...");
                    s.shutdown(Shutdown::Both)?;
                    break;
                } else if buffer.starts_with("disconnect") {
                    println!("Breaking connection...");
                    if let Some(s) = stream.take() {
                        s.shutdown(Shutdown::Both)?;
                    }

                    let line = format!("DISCONNECTED from {:#?}:{:#?}",
                                       current_server_addr.unwrap_or_default(),
                                       current_port.unwrap_or_default());
                    match write_to_file(line.as_str()) {
                        Ok(_) => {},
                        Err(e) => eprintln!("Error writing to file: {}", e),
                    }
                    break 'main_loop;
                }

                s.write_all(buffer.as_bytes())?;
                buffer.clear();

                let mut response_buffer = [0; 1024];
                match s.read(&mut response_buffer) {
                    Ok(n) if n > 0 => {
                        let response = str::from_utf8(&response_buffer[..n]).unwrap();
                        println!("S=>C: {}", response);

                        let line = format!("S=>C: {}", response);
                        match write_to_file(line.as_str()) {
                            Ok(_) => {},
                            Err(e) => eprintln!("Error writing to file: {}", e),
                        }
                    }
                    Ok(_) | Err(_) => {
                        println!("Connection lost");
                        let line = format!("DISCONNECTED from {:#?}:{:#?}",
                                           current_server_addr.unwrap_or_default(),
                                           current_port.unwrap_or_default());
                        match write_to_file(line.as_str()) {
                            Ok(_) => {},
                            Err(e) => eprintln!("Error writing to file: {}", e),
                        }
                        break 'main_loop;
                    }
                }
            }
        }
    }
    Ok(())
}
