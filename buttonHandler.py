class ButtonHandler:
    def __init__(self, buttonType, **kwargs):
        self.buttonType = buttonType  # 'rectangle', 'circle', or 'rounded'
        self.name = kwargs.get("name")
        if buttonType == "rectangle":
            self.x = kwargs.get("x")
            self.y = kwargs.get("y")
            self.width = kwargs.get("width")
            self.height = kwargs.get("height")
        elif buttonType == "circle":
            self.cx = kwargs.get("cx")
            self.cy = kwargs.get("cy")
            self.radius = kwargs.get("radius")
        elif buttonType == "rounded":
            self.x = kwargs.get("x")
            self.y = kwargs.get("y")
            self.width = kwargs.get("width")
            self.height = kwargs.get("height")
            self.radius = kwargs.get("radius")
        else:
            raise ValueError("Invalid button type. Use 'rectangle', 'circle', or 'rounded'.")

    def isClicked(self, mouseX, mouseY):
        if self.buttonType == "rectangle":
            return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height
        elif self.buttonType == "circle":
            return ((mouseX - self.cx) ** 2 + (mouseY - self.cy) ** 2) ** 0.5 <= self.radius
        elif self.buttonType == "rounded":
            # Check for clicks in the rectangular center
            if self.x + self.radius <= mouseX <= self.x + self.width - self.radius and self.y <= mouseY <= self.y + self.height:
                return True
            # Check for clicks in the top or bottom horizontal rectangle extensions
            elif self.x <= mouseX <= self.x + self.width and self.y + self.radius <= mouseY <= self.y + self.height - self.radius:
                return True
            # Check for clicks in the four corner circles
            elif ((mouseX - (self.x + self.radius)) ** 2 + (mouseY - (self.y + self.radius)) ** 2) ** 0.5 <= self.radius:
                return True  # Top-left corner
            elif ((mouseX - (self.x + self.width - self.radius)) ** 2 + (mouseY - (self.y + self.radius)) ** 2) ** 0.5 <= self.radius:
                return True  # Top-right corner
            elif ((mouseX - (self.x + self.radius)) ** 2 + (mouseY - (self.y + self.height - self.radius)) ** 2) ** 0.5 <= self.radius:
                return True  # Bottom-left corner
            elif ((mouseX - (self.x + self.width - self.radius)) ** 2 + (mouseY - (self.y + self.height - self.radius)) ** 2) ** 0.5 <= self.radius:
                return True  # Bottom-right corner
            return False
