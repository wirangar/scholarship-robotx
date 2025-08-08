from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.logger import log_action

router = Router()

# Define FSM States for ISEE calculation
class IseeForm(StatesGroup):
    waiting_for_income = State()
    waiting_for_property_size = State()
    waiting_for_family_members = State()

# Handler to start the ISEE calculation flow
@router.message(Command("isee"))
async def cmd_isee(message: types.Message, state: FSMContext):
    """
    Starts the ISEE calculation process.
    """
    log_action("isee_command_start", message.from_user.id)
    await state.set_state(IseeForm.waiting_for_income)
    await message.reply(
        "Let's calculate an estimate of your ISEE.\n"
        "Please enter your total annual family income in Euros (€)."
    )

# Handler for the income
@router.message(IseeForm.waiting_for_income, F.text)
async def process_income(message: types.Message, state: FSMContext):
    """
    Processes the family income and asks for the next piece of information.
    """
    try:
        income = float(message.text)
        await state.update_data(income=income)
        await state.set_state(IseeForm.waiting_for_property_size)
        await message.reply(
            "Great. Now, please enter the total size of family-owned property in square meters (m²)."
        )
    except ValueError:
        await message.reply("Please enter a valid number for the income (e.g., 15000).")

# Handler for the property size
@router.message(IseeForm.waiting_for_property_size, F.text)
async def process_property_size(message: types.Message, state: FSMContext):
    """
    Processes the property size and asks for the final piece of information.
    """
    try:
        property_size = float(message.text)
        await state.update_data(property_size=property_size)
        await state.set_state(IseeForm.waiting_for_family_members)
        await message.reply(
            "Got it. Finally, please enter the number of members in your family household."
        )
    except ValueError:
        await message.reply("Please enter a valid number for the property size (e.g., 80).")

from config import ISEE_THRESHOLD

def get_family_coefficient(members: int) -> float:
    """
    Determines the family coefficient based on the number of members.
    """
    coefficients = {1: 1.0, 2: 1.57, 3: 2.04, 4: 2.46, 5: 2.85}
    if members >= 5:
        # For more than 5 members, add 0.35 for each additional member
        return coefficients[5] + (0.35 * (members - 5))
    return coefficients.get(members, 1.0)

def calculate_isee_status(income: float, property_size: float, family_members: int) -> (float, str):
    """
    Calculates the ISEE value and determines the scholarship status.
    """
    family_coefficient = get_family_coefficient(family_members)

    # Formula: ISEE = (Income + (Property Value * 0.2)) / Family Coefficient
    # Property Value is estimated as size * 500
    property_value = property_size * 500
    isee = (income + (property_value * 0.2)) / family_coefficient

    if ISEE_THRESHOLD <= 0: # Avoid division by zero
        return isee, "ISEE threshold not configured."

    percentage = (isee / ISEE_THRESHOLD) * 100

    if percentage <= 55:
        status = "Full Scholarship"
    elif percentage <= 71.5:
        status = "Medium Scholarship"
    elif percentage <= 100:
        status = "Partial Scholarship"
    else:
        status = "Not Eligible"

    return isee, status

# Handler for the number of family members (final step)
@router.message(IseeForm.waiting_for_family_members, F.text)
async def process_family_members_and_calculate(message: types.Message, state: FSMContext):
    """
    Processes the final input, calculates the ISEE, and displays the result.
    """
    try:
        family_members = int(message.text)
        if family_members <= 0:
            raise ValueError("Family members must be a positive number.")
        await state.update_data(family_members=family_members)

        user_data = await state.get_data()

        isee_value, scholarship_status = calculate_isee_status(
            income=user_data.get("income", 0),
            property_size=user_data.get("property_size", 0),
            family_members=user_data.get("family_members", 1)
        )

        log_action("isee_calculated", message.from_user.id, f"ISEE: {isee_value:.2f}")

        result_text = (
            f"📈 **Your Estimated ISEE Result**\n\n"
            f"Calculated ISEE Value: **€{isee_value:,.2f}**\n"
            f"Scholarship Status: **{scholarship_status}**\n\n"
            f"*Disclaimer: This is only an estimate based on the provided formula. "
            f"The official ISEE must be calculated by a CAF or Patronato.*"
        )

        await message.reply(result_text, parse_mode="Markdown")
        await state.clear()

    except ValueError:
        await message.reply("Please enter a valid whole number for the family members (e.g., 4).")
