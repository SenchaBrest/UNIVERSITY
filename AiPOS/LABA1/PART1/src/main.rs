use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

use std::str;

fn handle_client(mut stream: TcpStream) {
    let mut buffer = [0; 1024];

    while let Ok(bytes_read) = stream.read(&mut buffer) {
        if bytes_read == 0 {
            break;
        }

        let input_str = str::from_utf8(&buffer[..bytes_read]).unwrap();

        if input_str.contains("..") {

            stream.write_all(b"Breaking connection...\n").unwrap();
            stream.shutdown(std::net::Shutdown::Both).unwrap();
            break;
        }

        let words: Vec<&str> = input_str.split_whitespace().collect();
        let reversed_words: Vec<&str> = words.iter().rev().copied().collect();
        let reversed_str = reversed_words.join(" ");

        stream.write_all(reversed_str.as_bytes()).unwrap();
    }
}

fn main() {
    let listener = TcpListener::bind("127.0.0.1:6666").expect("Failed to bind");
    println!("TCP SERVER DEMO - Listening on port 6666");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                println!("New connection from: {}", stream.peer_addr().unwrap());
                thread::spawn(|| {
                    handle_client(stream);
                });
            }
            Err(e) => {
                eprintln!("Error: {}", e);
            }
        }
    }
}