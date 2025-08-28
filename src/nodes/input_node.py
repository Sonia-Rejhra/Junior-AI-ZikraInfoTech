def receive_input(state):
    """
    Entry point node.
    Agar ticket user se already aaya ho (main.py se), to use karo.
    Warna ek default dummy ticket return karo.
    """
    if "ticket" not in state:
        ticket = {
            "subject": "Unable to reset password",
            "description": "I tried multiple times but the reset link never arrives."
        }
        state["ticket"] = ticket

    print("\n📩 Received Ticket:", state["ticket"])
    return state
