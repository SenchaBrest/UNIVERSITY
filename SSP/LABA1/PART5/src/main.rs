fn main() {
    let text_array: Vec<String> = vec![
        String::from("1"),
        String::from("2"),
        String::from("3"),
    ];

    println!("Введите разделитель: ");
    let mut delimiter = String::new();
    std::io::stdin().read_line(&mut delimiter).expect("Не удалось считать строку");

    delimiter = delimiter.trim().to_string();

    let mut extracted_lines: Vec<String> = Vec::new();

    for line in &text_array {
        let split_lines: Vec<&str> = line.split(&delimiter).collect();
        for split_line in split_lines {
            extracted_lines.push(split_line.to_string());
        }
    }

    println!("Извлеченные строки:");
    for extracted_line in &extracted_lines {
        println!("{}", extracted_line);
    }
}
