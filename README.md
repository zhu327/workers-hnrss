# workers-hnrss

workers-hnrss is a project deployed on Cloudflare Workers that translates Hacker News RSS feeds into the target language using Microsoft Azure Translation API.

### Configuration

1. Clone the repository:

    ```bash
    git clone https://github.com/zhu327/workers-hnrss.git
    ```

2. Modify the `wrangler.toml` file to include the required environment variables for configuring the Microsoft Azure Translation API:

    ```toml
    [vars]
    TRANSLATE_API_KEY = "your-azure-translate-api-key"
    TRANSLATE_API_REGION = "your-azure-region"
    TRANSLATE_LANGUAGE = "your-target-language"
    ```

    Replace `your-azure-translate-api-key` with your Azure Translation API key, `your-azure-region` with the Azure region you're using, and `your-target-language` with the target language you want to translate to.

## Installation and Deployment

Before deploying the project, make sure to follow the [Cloudflare Workers Python documentation](https://developers.cloudflare.com/workers/languages/python/) for installation and deployment instructions.

```bash
npx wrangler@latest deploy
```

### Usage

To use the project, replace the Hacker News RSS feed URL on [hnrss.github.io](https://hnrss.github.io/) with the URL of your deployed Cloudflare Workers project. For example, if your project is deployed at `https://hn.you-account.workers.dev`, replace `https://hnrss.org/newest` with `https://hn.you-account.workers.dev/newest`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.