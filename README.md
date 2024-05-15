# Calling Avatar Bot
This sample demonstrates how to talk to your own personalized avatars on a phone call. This project is meant for banterai assignment. Refer the below video demo:

https://github.com/AashishKumar-3002/calling-avatar-bot/assets/110625812/dee0c34e-fd1a-4d0a-9240-c08386f5f521

To watch the video demo, navigate to the `static` folder of your local copy of the repository and open the file named `Demo-Video-banterai.mp4`.

## Sign-up to Deepgram , elevenlabs and anthropic

Before you start, it's essential to generate a Deepgram API key to use in this project. [Sign-up now for Deepgram and create an API key](https://console.deepgram.com/signup?jump=keys).

You will also need to sign up for an account with [elevenlabs](https://elevenlabs.com/) and [anthropic](https://anthropic.com/).

## Quickstart

### Manual

Follow these steps to get started with this starter application.

#### Clone the repository

Go to GitHub and [clone the repository](https://github.com/AashishKumar-3002/calling-avatar-bot.git).

#### Install dependencies

Install the project dependencies.

```bash
pip install -r requirements.txt
```

#### Edit the config file

Copy the code from `sample.env` and create a new file called `.env`. Paste in the code and enter your API key you generated in the above steps

```js
DEEPGRAM_API_KEY=%api_key%
ELEVENLABS_API_KEY=%api_key%
ANTHROPIC_API_KEY=%api_key%
```

#### Run the application

Once running, you can access the application in your browser at <http://127.0.0.1:5000> or <http://localhost:5000>.

```bash
python app.py
```



## Issue Reporting

If you have found a bug or if you have a feature request, please report them at this repository issues section. 

## Getting Help

I would love to hear from you so if you have questions, comments or find a bug in the project, let us know! 

## Author

[Aashish Kumar](https://www.linkedin.com/in/aashish-kumar-iiit/)

## License

This project is licensed under the MIT license. See the [LICENSE](./LICENSE) file for more info.
