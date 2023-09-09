fn main() {
    let text = String::from("Text with vowels and spaces");

    let char_collection: Vec<char> = text.chars().collect();

    fn is_vowel(c: char) -> bool {
        matches!(c, 'a' | 'e' | 'i' | 'o' | 'u' | 'y' |
                    'A' | 'E' | 'I' | 'O' | 'U' | 'Y' )
    }

    let mut vowel_count = 0;
    let mut space_count = 0;

    for &c in &char_collection {
        if is_vowel(c) {
            vowel_count += 1;
        } else if c == ' ' {
            space_count += 1;
        }
    }

    let total_letter_count = char_collection.len() - space_count;

    println!("Input: {}", text);
    println!("Amount of vowel letters: {}", vowel_count);
    println!("Amount of spaces: {}", space_count);
    println!("Amount of letters: {}", total_letter_count);
}
