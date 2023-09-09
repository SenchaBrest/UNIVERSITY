use rand::Rng;

fn main() {
    let months = [
        "январь", "февраль", "март", "апрель", "май", "июнь",
        "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
    ];

    let mut rng = rand::thread_rng();
    let mut values = [0.0; 12];
    for i in 0..12 {
        values[i] = rng.gen_range(0.0..100.0);
    }

    for i in 0..12 {
        println!("{}: {:.2}", months[i], values[i]);
    }

    let sum: f64 = values.iter().sum();
    let average = sum / 12.0;
    println!("Среднее значение: {:.2}", average);
}
