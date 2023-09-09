/*use std::fs::File;
use std::io::{self, Write};
use rand::Rng;

fn main() -> io::Result<()> {
    let count = rand::thread_rng().gen_range(1..=1000000);

    let mut file = File::create("random_numbers.txt")?;

    write!(file, "{}\n", count)?;

    for _ in 0..count {
        let num = rand::thread_rng().gen_range(1..=1000);
        write!(file, "{}\n", num)?;
    }

    println!("The file 'random_numbers.txt' was successfully created and filled in.");

    Ok(())
}*/


use std::env;
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};

fn main() -> Result<(), Box<dyn Error>> {

    let args: Vec<String> = env::args().collect();

    if args.len() != 3 {
        eprintln!("Usage: {} <input_file> <sort_order>", args[0]);
        std::process::exit(1);
    }

    let input_file = &args[1];
    let sort_order = &args[2];

    let file = File::open(input_file)?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines();
    let _ = lines.next();

    let mut numbers: Vec<u32> = lines
        .filter_map(|line| line.ok())
        .filter_map(|line| line.parse().ok())
        .collect();

    match sort_order.as_str() {
        "asc" => numbers.sort(),
        "desc" => numbers.sort_by(|a, b| b.cmp(a)),
        _ => {
            eprintln!("Invalid collation: {}", sort_order);
            std::process::exit(1);
        }
    }

    let output_file_name = "output.txt";
    let mut output_file = File::create(output_file_name)?;

    for num in &numbers {
        writeln!(output_file, "{}", num)?;
    }

    println!("The data was successfully sorted and written to the file '{}'",
             output_file_name);

    Ok(())
}
