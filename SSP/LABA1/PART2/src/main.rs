fn main() {
    let dates: [&str; 10] = [
        "01/09/2022", "15/05/2023", "30/11/2022", "07/03/2024", "20/12/2023",
        "10/08/2022", "25/06/2023", "18/10/2024", "12/04/2022", "05/07/2023",
    ];

    let months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ];

    for date in &dates {
        let parts: Vec<&str> = date.split('/').collect();

        if parts.len() == 3 {
            if let (Ok(day), Ok(month), Ok(year)) = (
                parts[0].parse::<usize>(),
                parts[1].parse::<usize>(),
                parts[2].parse::<usize>(),
            ) {
                if month >= 1 && month <= 12 {
                    println!("{:02} {} {}", day, months[month - 1], year);
                } else {
                    println!("Ошибка: Некорректный месяц: {}", month);
                }
            } else {
                println!("Ошибка: Неверный формат даты: {}", date);
            }
        } else {
            println!("Ошибка: Неверный формат даты: {}", date);
        }
    }
}
