mod eke;
use eke::{generate_private_key, compute_public_key, compute_shared_secret};

use num_bigint::BigUint;
use std::io::{self, BufRead, Write, Read};
use std::net::TcpStream;
use byteorder::{BigEndian, ReadBytesExt, WriteBytesExt};
use rc4::Cipher;

fn main() {
    match TcpStream::connect("127.0.0.1:8081") {
        Ok(mut server) => {
            let prime = receive_biguint(&mut server);
            let generator = receive_biguint(&mut server);

            let client_private_key = generate_private_key(&prime);
            let client_public_key = compute_public_key(&generator, &prime, &client_private_key);

            send_biguint(&mut server, &client_public_key);

            let server_public_key = receive_biguint(&mut server);

            let shared_secret = compute_shared_secret(&server_public_key, &prime, &client_private_key);
            println!("Shared secret: {}", shared_secret);

            let mut rc4 = rc4::Cipher::new(&shared_secret.to_bytes_be()).unwrap();

            handle_server(&mut rc4, &mut server);
        }
        Err(e) => {
            eprintln!("Error connecting to server: {}", e);
        }
    }
}

fn handle_server(rc4: &mut Cipher, server: &mut TcpStream) {
    let stdin = io::stdin();
    let mut reader = stdin.lock();
    let mut buffer = String::new();
    loop {
        reader.read_line(&mut buffer).expect("Error reading line from console");
        let mut dst: Vec<u8> = vec![0; buffer.len()];
        rc4.xor(buffer.as_bytes(), &mut dst);

        server.write_all(&dst).expect("Error sending data");
        buffer.clear();
    }
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
