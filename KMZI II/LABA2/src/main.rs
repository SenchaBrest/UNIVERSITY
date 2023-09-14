mod lib;
use lib::{Digest, Ripemd256};
use std::env;
use std::fs;
use std::io::{self, Read};

const BUFFER_SIZE: usize = 1024;

/// Print digest result as hex string and name pair
fn print_result(sum: &[u8], name: &str) {
    for byte in sum {
        print!("{:02x}", byte);
    }
    println!("\t{}", name);
}

/// Compute digest value for given `Reader` and print it
/// On any error simply return without doing anything
fn process<D: Digest + Default, R: Read>(reader: &mut R, name: &str) {
    let mut sh = D::default();
    let mut buffer = [0u8; BUFFER_SIZE];
    loop {
        let n = match reader.read(&mut buffer) {
            Ok(n) => n,
            Err(_) => return,
        };
        sh.update(&buffer[..n]);
        if n == 0 || n < BUFFER_SIZE {
            break;
        }
    }
    print_result(&sh.finalize(), name);
}


fn main() {
    let args: Vec<String> = env::args().collect();
    // Process files listed in command line arguments one by one
    // If no files provided process input from stdin
    if args.len() > 2 {
        let path = args[1].clone();
        match args[2].clone().parse::<i32>() {
            Ok(rev) => {
                if let Ok(mut file) = fs::File::open(&path) {
                    let mut contents = String::new();
                    let _ = file.read_to_string(&mut contents);

                    if let Some(byte_index) = rev.checked_div(8) {
                        if let Some(byte_index_usize) =
                                        <i32 as TryInto<usize>>::try_into(byte_index).ok()  {
                            if byte_index_usize < contents.len() {
                                let mut byte = contents.as_bytes()[byte_index_usize];
                                let bit_to_set = rev % 8;
                                byte ^= 1 << bit_to_set;
                                unsafe {
                                    contents.as_bytes_mut()[byte_index_usize] = byte;
                                }
                            }
                        } else {
                            eprintln!("The bit index is beyond the length of the string.");
                        }
                    } else {
                        eprintln!("Bit index must be greater than or equal to 0.");
                    }

                    process::<Ripemd256, _>(&mut contents.as_bytes(), &path);
                } else {
                    println!("Failed to open file: {}", path);
                }
            }
            Err(e) => {
                eprintln!("{}", e);
            }
        }
    } else if args.len() == 2 {
        let path = args[1].clone();
        if let Ok(mut file) = fs::File::open(&path) {
            process::<Ripemd256, _>(&mut file, &path);
        }
    } else {
        process::<Ripemd256, _>(&mut io::stdin(), "-");
    }
}
