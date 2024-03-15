# Quasar Chess Engine

Welcome to the Quasar Chess Engine repository! This project aims to develop a chess engine capable of playing on an infinite chessboard. Traditional chess is played on an 8x8 board, but this engine extends the concept to allow for virtually limitless board sizes.

## Features

(Wait for v0.1.0)

## Installation

To run the Quasar Chess Engine, ensure you have [Python](https://www.python.org/) installed on your system. Then, follow these steps:

1. Clone this repository to your local machine:

   ```zsh
   git clone https://github.com/your-username/quasar-chess-engine.git
   ```

2. Create virtual environment:

   ```zsh
   pyhton -m venv quasar-chess-engine
   ```

3. Navigate to the project directory:

   ```zsh
   cd quasar-chess-engine
   ```

4. Change source python:

   ```zsh
   source bin/activate
   ```

5. Install dependencies:

   ```zsh
   pip install -r requirements.txt
   ```

## Usage

1. Start a game by running:

   ```zsh
   bin/python quasar/main.py run
   ```

2. To check other functionalities of the program run:

   ```zsh
   bin/python quasar/main.py -h
   ```

3. Enjoy playing chess on an infinite board!

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a new Pull Request.

Please note that after you add features, **all of the tests** have to pass without any assertion errors.

## Tests

Tests are crucial to maintain quality and integrity of the project. To run them:

```zsh
bin/python main.py test
```

There are three types of tests:
   
1. Quick tests (-qt)

   - Use these during development to check quickly if features that you're adding are compatible with existing code. Quick tests don't check some of the more computationaly demanding features. Run them by using -qt or --quick-test flags.

2. Standard tests (-st)

   - These tests are necessary to check before creating a pull request. To run standard tests you don't have to use any flags but -st or --standard-test will also work.

3. Full tests (-ft)

   - TBA

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Thanks to Naviary for propagating the idea of infinite chess and to the [Infinite Chess](https://discord.gg/8dCgAPt9v8) discord server for help and feedback.
- Special thanks to all contributors to this project.

## Contact

For any questions or feedback, feel free to reach out on [discord](https://discord.gg/8dCgAPt9v8) or [email](mailto:tymon.becella@gmail.com).
