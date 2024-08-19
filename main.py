import configuration
import gai
from nicegui import ui
#### LOWMAN DATA PROVIDED BY LOWMAN-CENTRAL.COM ####

def main():
    """
    handling gui

    """
    ui.run(dark=True, title='The Destiny Resume')
    with ui.header(elevated=True).classes('items-center justify-between'):
        # Create a text input field
        ui.label("The Destiny Resume").style('font-size: 200%')
        text_input = ui.input(label='Ex: khazicus#9648').style('font-size: 200%')
        
        # Create a button to submit name
        ui.button('Generate', on_click=lambda: handle_submit(text_input.value))

        ui.link("GitHub", 'https://github.com/ChasePoin/The-Destiny-Resume-Public').style('font-size: 200%; color: #FFFFFF')
    # Display the result
    result_label = ui.label().style('white-space: pre-wrap')
    # Define the function to handle the submit button click
    def handle_submit(input_value):
        input_value = str(input_value)
        processed_value = connection(input_value)
        result_label.set_text(processed_value)

def connection(name):
    """
    connection from website to backend, handles everything

    """
    # sets up AI
    model = gai.configureAI()
    # sets up user (gets user stats, translates them)
    user_setup = configuration.UserSetup(name)
    user_setup.fullUserSetup()
    # creates the description for the AI
    userDescriptor = configuration.UserDescriptors(user_setup.user)
    description = userDescriptor.create_user_desc()
    # sends the description to gemini
    response = gai.sendPrompt(model, description)
    # write to resume text file
    return response.text

if __name__ == "__main__":
    main()


# to do: make api endpoint generator function so that grabbers is less ugly...
# to do: find a way to get back currency and date of birth
