# idcard.py

from PIL import Image, ImageDraw, ImageFont

def generate_id_card(appointment, filename="id_card.png"):
    """
    Generate an ID card for a given appointment.
    
    Parameters:
    - appointment: dict with 'name', 'date_time', and 'reason'
    - filename: file path to save the card
    """
    # Card size
    width, height = 400, 250
    card = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(card)

    # Load fonts
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font_large = font_small = ImageFont.load_default()

    # Draw border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline='black', width=2)

    # Draw text
    draw.text((20, 20), f"Name: {appointment['name']}", font=font_large, fill='black')
    draw.text((20, 80), f"Date & Time: {appointment['date_time']}", font=font_small, fill='black')
    draw.text((20, 140), f"Reason: {appointment['reason']}", font=font_small, fill='black')

    # Save the ID card
    card.save(filename)
    print(f"Saved ID card as: {filename}")
