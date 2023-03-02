import openai
import csv
import os

# https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key
openai.api_key = os.environ.get('OPENAI_API_KEY')
username = 'James'

def get_response(chat):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat
    )
    return response['choices'][0]['message']['content']

def main():
    print(f'Welcome to the ChatGPT command line tool!\n')
    history = [{'role': 'system', 'content': f'You are a helpful assistant.'}]

    while True:
        user_input = input('> ' + username + ': ').strip()
        if not user_input:
            print('Input cannot be empty!')
            continue
        print()
        if user_input.lower() == 'exit':
            history.append({'role': 'user', 'content': 'summarize the entire conversation in one sentence with less than or equal to 4 words'})
            if not os.path.exists('chat_history/'):
                os.makedirs('chat_history/')
            summary = get_response(history[1:]).replace(' ', '-')
            f_path = 'chat_history/' + summary + 'csv'
            with open(f_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['role', 'content'])
                writer.writeheader()
                for row in history[1:-1]:
                    writer.writerow(row)
                print('Conversation history saved to', f_path)
            break
        history.append({'role': 'user', 'content': user_input})
        rsp_content = get_response(history)
        print(f'> ChatGPT: {rsp_content}\n')
        history.append({'role': 'assistant', 'content': rsp_content})

if __name__ == '__main__':
    main()
