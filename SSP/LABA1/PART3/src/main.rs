extern crate rand;

use rand::Rng;

fn main() {
    let n = 10;

    let consonants = "bcdfghjklmnpqrstvwxz";

    let mut rng = rand::thread_rng();
    let mut result = String::new();

    for _ in 0..n {
        let index = rng.gen_range(0..consonants.len());
        let consonant = &consonants[index..index + 1];
        result.push_str(consonant);
    }

    println!("Random sequence of consonant letters: {}", result);
}
