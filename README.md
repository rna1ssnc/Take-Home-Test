Running the Project:

1. Backend Setup:
   - Open VSCode and access the terminal (Bash).
   - Execute the following commands sequentially:
     ```bash
     python activity.py -n 10 -f json
     python activity.py -n 5 -f csv
     python activity.py -n 15 -f console
     ```

2. Start the Server:
   - In the same terminal, run:
     ```bash
     python server.py
     ```

3. Frontend Setup:
   - Open a new terminal (Bash).
   - Serve the frontend using a simple HTTP server with:
     ```bash
     python -m http.server 5500
     ```

4. View the Frontend:
   - In VSCode, right-click `index.html` and select "Open with Live Server."
   - This action will open the web page in your default browser.

5. Interact with the Web Page:
   - The data will be displayed in a table on the web page.
   - You can choose to download data in JSON or CSV format, or print it to the console using the provided options.
