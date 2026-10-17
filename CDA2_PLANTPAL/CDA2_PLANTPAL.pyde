"""
PLANTPAL - BEGINNER-FRIENDLY PROCESSING PYTHON PROJECT

This program uses:
1. Variables to store cups, streaks and plants.
2. If statements to make decisions.
3. Loops to draw repeated objects.
4. Functions to organise the code.
5. mousePressed() to create clickable buttons.

No imports, libraries or image files are required.
"""


# ---------------- SETTINGS AND VARIABLES ----------------

DAILY_GOAL = 8

PLANT_NAMES = [
    "Daisy",
    "Sunflower",
    "Tulip"
]

# App colours
BACKGROUND_COLOUR = (238, 243, 229)
WHITE = (255, 255, 255)
GREEN = (90, 141, 59)
DARK_GREEN = (47, 90, 44)
TEXT_GREEN = (85, 112, 72)
BLUE = (101, 184, 209)

# 0 means the Today screen.
# 1 means the Garden screen.
current_screen = 0

cups = 0
streak = 0
selected_plant = 0

last_completed = ""
last_opened_date = ""

# Each saved plant contains its type and date.
garden = []

# Reminder timer variables
timer_running = False
timer_minutes = 30
timer_ends_at = 0

heading_font = None
body_font = None


# ---------------- PROGRAM SETUP ----------------

def setup():
    global heading_font, body_font

    size(430, 800)
    smooth(8)

    heading_font = createFont("Georgia", 32)
    body_font = createFont("Arial", 16)

    load_progress()
    check_new_day()


# draw() continuously updates the screen.
def draw():
    background(*BACKGROUND_COLOUR)

    if current_screen == 0:
        draw_today_screen()
    else:
        draw_garden_screen()

    draw_bottom_navigation()
    check_timer()


# ---------------- TODAY SCREEN ----------------

def draw_today_screen():
    draw_header(
        "PlantPal",
        "Grow a garden, one glass at a time"
    )

    draw_streak_card()
    draw_timer_card()
    draw_growing_card()
    draw_drink_button()
    draw_timer_buttons()


def draw_streak_card():
    card(24, 104, 180, 72, 16, WHITE)

    fill(*DARK_GREEN)
    textFont(body_font)
    textSize(11)
    textAlign(LEFT)
    text("CURRENT STREAK", 40, 129)

    if streak == 1:
        day_word = "day"
    else:
        day_word = "days"

    textFont(heading_font)
    textSize(22)
    text(
        str(streak) + " " + day_word,
        40,
        157
    )


def draw_timer_card():
    card(218, 104, 188, 72, 16, WHITE)

    fill(*DARK_GREEN)
    textFont(body_font)
    textSize(11)
    textAlign(LEFT)
    text("HYDRATION SESSION", 234, 129)

    textSize(16)
    text(timer_text(), 234, 156)


def draw_growing_card():
    card(24, 190, 382, 397, 24, WHITE)

    # Plant name
    fill(*DARK_GREEN)
    textAlign(CENTER)
    textFont(heading_font)
    textSize(23)

    text(
        PLANT_NAMES[selected_plant],
        width / 2,
        226
    )

    # Plant selection arrows
    draw_selector_button(53, 265, False)
    draw_selector_button(377, 265, True)

    # Background circle
    noStroke()
    fill(234, 244, 218)
    ellipse(width / 2, 376, 214, 214)

    # Grass
    fill(168, 199, 124)
    arc(
        width / 2,
        418,
        205,
        105,
        PI,
        TWO_PI
    )

    draw_progress_circle()

    # Draw the selected plant
    draw_plant(
        width / 2,
        434,
        cups,
        selected_plant,
        0.85
    )

    draw_progress_message()
    draw_water_drops()


def draw_progress_circle():
    # Empty progress circle
    noFill()
    stroke(213, 224, 201)
    strokeWeight(9)

    ellipse(
        width / 2,
        376,
        226,
        226
    )

    # Completed part of the circle
    stroke(*GREEN)

    progress = TWO_PI * cups / float(DAILY_GOAL)

    arc(
        width / 2,
        376,
        226,
        226,
        -HALF_PI,
        -HALF_PI + progress
    )

    noStroke()


def draw_progress_message():
    fill(*DARK_GREEN)
    textFont(body_font)
    textSize(14)
    textAlign(CENTER)

    cups_remaining = DAILY_GOAL - cups

    if cups_remaining == 0:
        message = "Your plant is safely in the garden!"
    elif cups_remaining == 1:
        message = "1 cup until it blooms"
    else:
        message = (
            str(cups_remaining)
            + " cups until it blooms"
        )

    text(message, width / 2, 510)


def draw_water_drops():
    # Draw eight water drops.
    for index in range(DAILY_GOAL):
        x = 104 + index * 32

        if index < cups:
            drop_colour = BLUE
        else:
            drop_colour = (200, 214, 192)

        draw_drop(
            x,
            543,
            drop_colour,
            0.62
        )

    fill(*TEXT_GREEN)
    textSize(12)
    textAlign(CENTER)

    text(
        str(cups)
        + " / "
        + str(DAILY_GOAL)
        + " cups today",
        width / 2,
        574
    )


def draw_drink_button():
    goal_complete = cups >= DAILY_GOAL

    if goal_complete:
        button_colour = (168, 184, 154)
        button_text = "Goal complete"
    else:
        button_colour = GREEN
        button_text = "+  I drank a cup"

    draw_button(
        24,
        605,
        382,
        60,
        button_colour,
        button_text
    )


def draw_timer_buttons():
    fill(*TEXT_GREEN)
    textAlign(LEFT)
    textSize(12)

    text(
        "30-minute grow session",
        30,
        703
    )

    if timer_running:
        timer_button_text = "Pause"
    else:
        timer_button_text = "Start"

    draw_small_button(
        207,
        680,
        94,
        38,
        timer_button_text
    )

    draw_small_button(
        311,
        680,
        94,
        38,
        "Reset"
    )


# ---------------- GARDEN SCREEN ----------------

def draw_garden_screen():
    draw_header(
        "My Garden",
        "Every completed day plants a memory"
    )

    card(24, 104, 382, 70, 16, WHITE)

    fill(*DARK_GREEN)
    textAlign(LEFT)
    textFont(heading_font)
    textSize(22)

    if len(garden) == 1:
        plant_word = "plant"
    else:
        plant_word = "plants"

    text(
        str(len(garden))
        + " "
        + plant_word
        + " grown",
        42,
        148
    )

    if len(garden) == 0:
        draw_empty_garden()
    else:
        draw_saved_plants()


def draw_empty_garden():
    draw_plant(
        width / 2,
        400,
        2,
        selected_plant,
        1.0
    )

    fill(*TEXT_GREEN)
    textAlign(CENTER)
    textFont(body_font)
    textSize(16)

    text(
        "Your garden is waiting to grow.",
        width / 2,
        480
    )

    textSize(13)

    text(
        "Drink 8 cups today to plant your first flower.",
        width / 2,
        507
    )


def draw_saved_plants():
    # Only show the 12 most recent plants.
    visible_plants = min(len(garden), 12)

    for index in range(visible_plants):
        item = garden[len(garden) - 1 - index]

        column = index % 3
        row = index // 3

        x = 86 + column * 129
        y = 275 + row * 126

        plant_type = int(item[0])
        plant_type = constrain(plant_type, 0, 2)

        draw_plant(
            x,
            y,
            DAILY_GOAL,
            plant_type,
            0.52
        )

        fill(*TEXT_GREEN)
        textFont(body_font)
        textSize(10)
        textAlign(CENTER)

        text(
            short_date(item[1]),
            x,
            y + 38
        )


# ---------------- SHARED INTERFACE ----------------

def draw_header(title, subtitle):
    noStroke()
    fill(*DARK_GREEN)
    rect(0, 0, width, 88)

    fill(*WHITE)
    textAlign(LEFT)
    textFont(heading_font)
    textSize(30)
    text(title, 24, 46)

    fill(217, 232, 207)
    textFont(body_font)
    textSize(12)
    text(subtitle, 25, 69)

    # Number of plants collected
    fill(71, 116, 56)
    rect(344, 24, 62, 34, 14)

    fill(*WHITE)
    textAlign(CENTER)
    textSize(13)

    text(
        "Plants: " + str(len(garden)),
        375,
        46
    )


def draw_bottom_navigation():
    noStroke()
    fill(*WHITE)
    rect(0, 738, width, 62)

    inactive_colour = (138, 151, 129)

    if current_screen == 0:
        today_colour = DARK_GREEN
        garden_colour = inactive_colour
    else:
        today_colour = inactive_colour
        garden_colour = DARK_GREEN

    fill(*today_colour)
    ellipse(126, 757, 8, 8)

    fill(*garden_colour)
    ellipse(304, 757, 8, 8)

    textFont(body_font)
    textSize(12)
    textAlign(CENTER)

    fill(*today_colour)
    text("Today", 126, 784)

    fill(*garden_colour)
    text("Garden", 304, 784)


def card(x, y, card_width, card_height,
         corner_radius, card_colour):
    noStroke()
    fill(*card_colour)

    rect(
        x,
        y,
        card_width,
        card_height,
        corner_radius
    )


def draw_button(x, y, button_width,
                button_height, button_colour,
                label):
    noStroke()
    fill(*button_colour)

    rect(
        x,
        y,
        button_width,
        button_height,
        18
    )

    fill(*WHITE)
    textFont(body_font)
    textSize(17)
    textAlign(CENTER)

    text(
        label,
        x + button_width / 2,
        y + 38
    )


def draw_small_button(x, y, button_width,
                      button_height, label):
    noStroke()
    fill(221, 232, 197)

    rect(
        x,
        y,
        button_width,
        button_height,
        13
    )

    fill(*DARK_GREEN)
    textFont(body_font)
    textSize(12)
    textAlign(CENTER)

    text(
        label,
        x + button_width / 2,
        y + 24
    )


def draw_selector_button(x, y, points_right):
    noStroke()
    fill(238, 243, 229)
    ellipse(x, y, 40, 40)

    fill(*GREEN)
    textFont(body_font)
    textSize(23)
    textAlign(CENTER)

    if points_right:
        arrow = ">"
    else:
        arrow = "<"

    text(arrow, x, y + 8)


# ---------------- PLANT DRAWING ----------------

def draw_plant(x, ground_y, stage,
               plant_type, scale_amount):
    pushMatrix()

    translate(x, ground_y)
    scale(scale_amount)
    noStroke()

    draw_pot()

    if stage > 0:
        stem_height = map(
            stage,
            1,
            DAILY_GOAL,
            25,
            125
        )

        # Draw the stem
        stroke(*GREEN)
        strokeWeight(6)
        line(0, 0, 0, -stem_height)
        noStroke()

        # Leaves appear as the user drinks water.
        if stage >= 2:
            draw_leaf(
                -2,
                -stem_height * 0.42,
                -1
            )

        if stage >= 4:
            draw_leaf(
                2,
                -stem_height * 0.65,
                1
            )

        if stage >= 6:
            draw_leaf(
                -2,
                -stem_height * 0.82,
                -1
            )

        # The flower appears after eight cups.
        if stage >= DAILY_GOAL:
            draw_flower(
                0,
                -stem_height,
                plant_type
            )
        else:
            fill(120, 169, 87)

            ellipse(
                0,
                -stem_height,
                18 + stage,
                14 + stage / 2
            )

    popMatrix()


def draw_pot():
    # Flowerpot
    fill(140, 92, 60)

    quad(
        -38, 0,
        38, 0,
        28, 54,
        -28, 54
    )

    # Soil
    fill(112, 68, 46)
    ellipse(0, 1, 78, 17)


def draw_leaf(x, y, direction):
    pushMatrix()

    translate(x, y)
    rotate(direction * 0.45)

    fill(120, 169, 87)

    ellipse(
        direction * 18,
        0,
        38,
        17
    )

    popMatrix()


def draw_flower(x, y, plant_type):
    pushMatrix()
    translate(x, y)

    if plant_type == 1:
        draw_sunflower()

    elif plant_type == 2:
        draw_tulip()

    else:
        draw_daisy()

    popMatrix()


def draw_sunflower():
    fill(247, 183, 51)

    # Draw 12 yellow petals.
    for index in range(12):
        pushMatrix()

        rotate(
            TWO_PI * index / 12.0
        )

        ellipse(0, -25, 16, 31)

        popMatrix()

    fill(107, 68, 39)
    ellipse(0, 0, 37, 37)


def draw_tulip():
    fill(241, 124, 141)

    beginShape()

    vertex(-27, 8)
    vertex(-24, -28)
    vertex(-8, -12)
    vertex(0, -35)
    vertex(9, -12)
    vertex(27, -28)
    vertex(23, 9)

    bezierVertex(
        18, 29,
        -18, 29,
        -27, 8
    )

    endShape(CLOSE)


def draw_daisy():
    fill(255, 253, 242)

    # Draw 10 white petals.
    for index in range(10):
        pushMatrix()

        rotate(
            TWO_PI * index / 10.0
        )

        ellipse(0, -23, 15, 30)

        popMatrix()

    fill(242, 201, 76)
    ellipse(0, 0, 31, 31)


def draw_drop(x, y, drop_colour,
              scale_amount):
    pushMatrix()

    translate(x, y)
    scale(scale_amount)

    noStroke()
    fill(*drop_colour)

    beginShape()

    vertex(0, -19)

    bezierVertex(
        -5, -9,
        -14, 0,
        -14, 10
    )

    bezierVertex(
        -14, 29,
        14, 29,
        14, 10
    )

    bezierVertex(
        14, 0,
        5, -9,
        0, -19
    )

    endShape(CLOSE)

    popMatrix()


# ---------------- MOUSE INTERACTION ----------------

# Processing automatically runs this function
# whenever the user clicks the mouse.
def mousePressed():
    global current_screen

    # Bottom navigation
    if mouseY > 738:
        if mouseX < width / 2:
            current_screen = 0
        else:
            current_screen = 1

        return

    # The remaining buttons only work
    # on the Today screen.
    if current_screen != 0:
        return

    # Previous plant button
    if dist(mouseX, mouseY, 53, 265) < 28:
        change_plant(-1)

    # Next plant button
    elif dist(mouseX, mouseY, 377, 265) < 28:
        change_plant(1)

    # Drink water button
    elif (inside(24, 605, 382, 60)
          and cups < DAILY_GOAL):
        log_cup()

    # Start or pause timer
    elif inside(207, 680, 94, 38):
        toggle_timer()

    # Reset timer
    elif inside(311, 680, 94, 38):
        reset_timer()


# Checks whether the mouse is inside a button.
def inside(x, y, button_width, button_height):
    inside_horizontally = (
        mouseX >= x
        and mouseX <= x + button_width
    )

    inside_vertically = (
        mouseY >= y
        and mouseY <= y + button_height
    )

    return (
        inside_horizontally
        and inside_vertically
    )


# ---------------- WATER AND PLANT LOGIC ----------------

def change_plant(direction):
    global selected_plant

    selected_plant += direction

    if selected_plant < 0:
        selected_plant = len(PLANT_NAMES) - 1

    if selected_plant >= len(PLANT_NAMES):
        selected_plant = 0

    save_progress()


def log_cup():
    global cups

    cups += 1

    if cups == DAILY_GOAL:
        complete_daily_goal()

    save_progress()


def complete_daily_goal():
    global streak, last_completed

    today = get_today()

    # Prevent the same plant from being
    # added more than once today.
    if today == last_completed:
        return

    # Start or increase the streak.
    if last_completed == "":
        streak = 1
    else:
        streak += 1

    # Save the new plant.
    new_plant = [
        selected_plant,
        today
    ]

    garden.append(new_plant)
    last_completed = today


# ---------------- REMINDER TIMER ----------------

def toggle_timer():
    global timer_running, timer_ends_at

    if timer_running:
        timer_running = False
    else:
        timer_running = True

        timer_ends_at = (
            millis()
            + timer_minutes * 60 * 1000
        )


def reset_timer():
    global timer_running, timer_ends_at

    timer_running = False
    timer_ends_at = 0


def check_timer():
    global timer_running

    if (timer_running
            and millis() >= timer_ends_at):

        timer_running = False

        surface.setTitle(
            "PlantPal - Time for water!"
        )


def timer_text():
    if not timer_running:
        return "Ready when you are"

    remaining = timer_ends_at - millis()
    remaining = max(0, remaining)

    total_seconds = remaining / 1000
    minutes_left = total_seconds / 60
    seconds_left = total_seconds % 60

    return (
        nf(minutes_left, 2)
        + ":"
        + nf(seconds_left, 2)
    )


# ---------------- SAVING PROGRESS ----------------

def check_new_day():
    global cups, last_opened_date

    today = get_today()

    saved_date = last_opened_date

    if saved_date == "":
        saved_date = last_completed

    # Reset cups when the date changes.
    if (saved_date != ""
            and saved_date != today):
        cups = 0

    last_opened_date = today

    save_progress()


def save_progress():
    # Save the main variables on the first line.
    first_line = (
        str(cups)
        + "|"
        + str(streak)
        + "|"
        + str(selected_plant)
        + "|"
        + last_completed
        + "|"
        + last_opened_date
    )

    lines = [first_line]

    # Save one plant on each following line.
    for item in garden:
        plant_line = (
            str(item[0])
            + "|"
            + item[1]
        )

        lines.append(plant_line)

    saveStrings(
        "data/plantpal_progress.txt",
        lines
    )


def load_progress():
    global cups
    global streak
    global selected_plant
    global last_completed
    global last_opened_date
    global garden

    try:
        lines = loadStrings(
            "plantpal_progress.txt"
        )

        if lines is None:
            return

        if len(lines) == 0:
            return

        # Load the main variables.
        settings = lines[0].split("|")

        cups = int(settings[0])
        streak = int(settings[1])

        selected_plant = (
            int(settings[2])
            % len(PLANT_NAMES)
        )

        if len(settings) > 3:
            last_completed = settings[3]

        if len(settings) > 4:
            last_opened_date = settings[4]

        # Load the saved garden.
        garden = []

        for line in lines[1:]:
            parts = line.split("|")

            if len(parts) == 2:
                saved_plant = [
                    int(parts[0]),
                    parts[1]
                ]

                garden.append(saved_plant)

    except:
        # Start fresh if the save file
        # cannot be opened.
        cups = 0
        streak = 0
        selected_plant = 0
        last_completed = ""
        last_opened_date = ""
        garden = []


# ---------------- DATE FUNCTIONS ----------------

def get_today():
    # Creates a date such as 2026-10-17.
    today = (
        str(year())
        + "-"
        + nf(month(), 2)
        + "-"
        + nf(day(), 2)
    )

    return today


def short_date(date_text):
    # Changes 2026-10-17 into 17 Oct.
    try:
        parts = date_text.split("-")

        month_names = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]

        month_number = int(parts[1])
        day_number = int(parts[2])

        return (
            str(day_number)
            + " "
            + month_names[month_number - 1]
        )

    except:
        return date_text
