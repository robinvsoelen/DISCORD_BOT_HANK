from openai import OpenAI
import requests
import discord
import requests
from discord.ext import commands
from discord import File

BOT_TOKEN = ""
openai_client = OpenAI(
    api_key="",
)

def getDallEImage(prompt):
    response = openai_client.images.generate(
    model="dall-e-2",
    prompt=prompt,
    size='1024x1024',
    quality="standard",
    n=1,
    )
    imageUrl = response.data[0].url
    imageLocalPath = 'images/intro-image.jpg'
    try:
        image = requests.get(imageUrl)
        if image.status_code == 200:
            with open(imageLocalPath, 'wb') as file:
                # Write the content of the response to the file
                file.write(image.content)
            print('Image successfully Downloaded: ', imageLocalPath)
            return imageLocalPath
        else:
            print('Image Couldn\'t be retrieved')
    except:
        print("FAIL")

    return ''

def getTextResponse(prompt):
    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": "This is a blog written by a knowledgable music enthousiast"},
        {"role": "user", "content": prompt},
    ]
    )

    response = completion.choices[0].message.content
    
    print(response)

    return response



intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Add this line
bot = commands.Bot(command_prefix='!', intents=intents) 

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='HANK', help='Responds to /HANK <message>')
async def hank_command(ctx, *args):
    message = ' '.join(args)  # This joins the list of words into a single string
    if not message:
        await ctx.send("You didn't provide a message!")
        return

    # Path to your image
    image_path = getDallEImage(message)

    # Send the image with a caption
    await ctx.send(content="", file=File(image_path))

# Run the bot
bot.run(BOT_TOKEN)
