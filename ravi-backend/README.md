# RAVI-backend

This is the backend for the RAVI project. It is built with FastAPI.

## Getting Started

1.  Clone the repository.
2.  Install dependencies: docker
3.  Replace key in ```secrets.yaml``` with your key.
4.  Run command:         ```cd ravi-backend``` 
                and then ```docker compose up --build```
5.  In new terminal:     ```cd ravi```
                and then ```npm install```
                and then ```npm run dev```

<!-- 4.  Start the server: `npm start` -->

## API Endpoints

*   `POST /ocr`: Takes in an image and gives OCR output.
*   `POST /tts`: Takes in text and returns audio.

## Development

*   Run in development mode: `npm run dev`
*   Run tests: `npm test`

## Deployment

The backend can be deployed to platforms like Heroku, Netlify, or Vercel.  Ensure environment variables are set correctly in the deployment environment.

## License

[MIT](LICENSE)
