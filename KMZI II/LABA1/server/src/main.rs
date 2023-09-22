mod eke;
use eke::{generate_prime, generate_private_key, compute_public_key, compute_shared_secret};

use num_bigint::BigUint;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;
use byteorder::{BigEndian, ReadBytesExt, WriteBytesExt};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:8080").expect("Failed to bind");

    for stream in listener.incoming() {
        match stream {
            Ok(mut client) => {
                let prime = generate_prime(512);
                let generator = BigUint::from(2u32);

                send_biguint(&mut client, &prime);
                send_biguint(&mut client, &generator);

                let client_public_key = receive_biguint(&mut client);

                let server_private_key = generate_private_key(&prime);
                let server_public_key = compute_public_key(&generator, &prime, &server_private_key);
                send_biguint(&mut client, &server_public_key);

                let shared_secret = compute_shared_secret(&client_public_key, &prime, &server_private_key);
                println!("Shared secret: {}", shared_secret);

                thread::spawn(move || {
                    handle_client(&mut client);
                });
            }
            Err(e) => {
                eprintln!("Error accepting connection: {}", e);
            }
        }
    }
}

fn handle_client(client: &mut TcpStream) {
    // code
}

fn send_biguint(stream: &mut dyn Write, num: &BigUint) {
    let num_bytes = num.to_bytes_be();

    stream.write_u64::<BigEndian>(num_bytes.len() as u64).unwrap();

    stream.write_all(&num_bytes).unwrap();
}

fn receive_biguint(stream: &mut dyn Read) -> BigUint {
    let size = stream.read_u64::<BigEndian>().unwrap() as usize;

    let mut num_bytes = vec![0; size];
    stream.read_exact(&mut num_bytes).unwrap();

    let num = BigUint::from_bytes_be(&num_bytes);

    num
}
