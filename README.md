# Telegram Bot for Applying to E-visa

This is a `E-visa bot` that allows `Users` to apply for `Dubai E-visa` through `Telegram`.

The bot collects all information, accepts payments and sends the application to the `Admin` for approval.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of `python`
* You have installed all the required packages from `requirements.txt`

## Installing Requirements

For installing packages from `requirements.txt` use the following command:

```
pip install -r requirements.txt
```

## Running Telegram Bot

To use Telegram Bot, just execute following:

```
python main.py
```

## Get Images from Image ID

Via the API's getFile you can get the required path information for the file:

```
https://api.telegram.org/bot<bot_token>/getFile?file_id=the_file_id
```

This will return an object with file_id, file_size and file_path. You can then use the file_path to download the file:

```
https://api.telegram.org/file/bot<token>/<file_path>
```

The maximum size of a file obtained through this method is 20MB. Error: Obtained when a file large than 20mb is used.(
Shown below)

```
{"ok":false,"error_code":400,"description":"Bad Request: file is too big[size:1556925644]"}
```

## Contact

If you want to contact me you can reach me at yura.yura.avagyan@gmail.com.

## License

All rights are reserved.