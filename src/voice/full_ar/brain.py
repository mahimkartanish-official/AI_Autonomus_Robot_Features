import datetime

class Brain:
    def process(self, text):
        text = text.lower()

        if "time" in text:
            return f"The time is {datetime.datetime.now().strftime('%H:%M')}"

        elif "hello" in text:
            return "Hello, how can I help you?"

        elif "forward" in text:
            return "Moving forward"  # later: ROS command

        return "I did not understand that."