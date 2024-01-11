import subprocess
import rospy
from robotiq_2f_gripper_control.msg import _Robotiq2FGripper_robot_output as outputMsg

from robot_servers.gripper_server import GripperServer


class RobotiqGripperServer(GripperServer):
    def __init__(self, gripper_ip):
        super().__init__()
        self.gripper = subprocess.Popen(
            [
                "rosrun",
                "robotiq_2f_gripper_control",
                "Robotiq2FGripperTcpNode.py",
                gripper_ip,
            ],
            stdout=subprocess.PIPE,
        )
        self.gripperpub = rospy.Publisher(
            "Robotiq2FGripperRobotOutput",
            outputMsg.Robotiq2FGripper_robot_output,
            queue_size=1,
        )
        self.gripper_command = outputMsg.Robotiq2FGripper_robot_output()

    def generate_gripper_command(self, char, command):
        """Update the gripper command according to the character entered by the user."""
        if char == "a":
            command = outputMsg.Robotiq2FGripper_robot_output()
            command.rACT = 1
            command.rGTO = 1
            command.rSP = 255
            command.rFR = 150

        if char == "r":
            command = outputMsg.Robotiq2FGripper_robot_output()
            command.rACT = 0

        if char == "c":
            command.rPR = 255

        if char == "o":
            command.rPR = 0

        # If the command entered is a int, assign this value to rPR
        # (i.e., move to this position)
        try:
            command.rPR = int(char)
            if command.rPR > 255:
                command.rPR = 255
            if command.rPR < 0:
                command.rPR = 0
        except ValueError:
            pass
        return command

    def activate_gripper(self):
        self.gripper_command = self.generate_gripper_command("a", self.gripper_command)
        self.gripperpub.publish(self.gripper_command)

    def reset_gripper(self):
        self.gripper_command = self.generate_gripper_command("r", self.gripper_command)
        self.gripperpub.publish(self.gripper_command)
        self.activate_gripper()

    def open(self):
        self.gripper_command = self.generate_gripper_command("o", self.gripper_command)
        self.gripperpub.publish(self.gripper_command)

    def close(self):
        self.gripper_command = self.generate_gripper_command("c", self.gripper_command)
        self.gripperpub.publish(self.gripper_command)

    def move(self, position):
        gripper_command = self.generate_gripper_command(position, self.gripper_command)
        self.gripperpub.publish(self.gripper_command)

    def update_gripper(self, msg):
        raise NotImplementedError("Not implemented for Robotiq Gripper")