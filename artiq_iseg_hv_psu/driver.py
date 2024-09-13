#!/usr/bin/env python3

import abc
import asyncio
import logging
import random
import socket


class ArtiqIsegHvPsuInterface(abc.ABC):
    @abc.abstractmethod
    async def set_channel_voltage(self, channel, voltage):
        pass

    @abc.abstractmethod
    async def set_channel_current(self, channel, current):
        pass

    @abc.abstractmethod
    async def get_channel_voltage(self, channel):
        pass

    @abc.abstractmethod
    async def get_channel_current(self, channel):
        pass

    @abc.abstractmethod
    async def get_channel_voltage_measured(self, channel):
        pass

    @abc.abstractmethod
    async def get_channel_current_measured(self, channel):
        pass

    @abc.abstractmethod
    async def set_channel_on(self, channel, channel_on):
        pass

    @abc.abstractmethod
    async def get_channel_on(self, channel):
        pass

    @abc.abstractmethod
    async def get_temperature(self):
        pass

    @abc.abstractmethod
    async def reset(self):
        pass

    async def ping(self):
        return True

    def close(self):
        pass


class ArtiqIsegHvPsu(ArtiqIsegHvPsuInterface):
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.device_ip, 10001))

    def send_command(self, command):
        self.client.send(bytes(command + "\r\n", "utf-8"))
        answer = self.client.recv(1024).decode("utf-8").replace("\r\n", "")
        return answer

    async def set_channel_voltage(self, channel, voltage):
        self.send_command(f":VOLT {voltage},(@{channel})")

    async def set_channel_current(self, channel, current):
        self.send_command(f":CURR {current},(@{channel})")

    async def set_channel_on(self, channel, channel_on):
        if channel_on:
            self.send_command(f":VOLT ON,(@{channel})")
        else:
            self.send_command(f":VOLT OFF,(@{channel})")

    async def get_channel_voltage(self, channel):
        return self.send_command(f":READ:VOLT?(@{channel})")

    async def get_channel_current(self, channel):
        return self.send_command(f":READ:CURR?(@{channel})")

    async def get_channel_voltage_measured(self, channel):
        return self.send_command(f":MEAS:VOLT?(@{channel})")

    async def get_channel_current_measured(self, channel):
        return self.send_command(f":MEAS:CURR?(@{channel})")

    async def get_channel_on(self, channel):
        channel_status = self.send_command(f":READ:CHAN:STAT? (@{channel})")
        channel_on = bool(int(channel_status) & (1 << 3))
        return channel_on

    async def get_temperature(self):
        temperature = self.send_command(":READ:MOD:TEMP?")
        return temperature

    async def reset(self):
        return self.send_command("*RST")

    def close(self):
        self.client.close()


class ArtiqIsegHvPsuSim(ArtiqIsegHvPsuInterface):
    def __init__(self):
        self.channel_voltage = 8 * [None]
        self.channel_current = 8 * [None]
        self.channel_on = 8 * [None]
        self.temperature = 42 + 10 * random.random()

    async def set_channel_voltage(self, channel, voltage):
        self.channel_voltage[channel] = voltage
        logging.warning(f"Simulated: Setting channel {channel} voltage to {voltage}")

    async def set_channel_current(self, channel, current):
        self.channel_current[channel] = current
        logging.warning(f"Simulated: Setting channel {channel} current to {current}")

    async def set_channel_on(self, channel, channel_on):
        self.channel_on[channel] = channel_on
        if channel_on:
            logging.warning("Simulated: Turning channel {channel} ON")
        else:
            logging.warning("Simulated: Turning channel {channel } OFF")

    async def get_channel_voltage(self, channel):
        logging.warning(
            f"Simulated: Channel {channel} voltage redout:"
            f"{self.channel_voltage[channel]}"
        )
        return self.channel_voltage[channel]

    async def get_channel_current(self, channel):
        logging.warning(
            f"Simulated: Channel {channel} current redout: "
            f"{self.channel_current[channel]}"
        )
        return self.channel_current[channel]

    async def get_channel_voltage_measured(self, channel):
        logging.warning(
            f"Simulated: Channel {channel} measured voltage redout: "
            f"{self.channel_voltage[channel] + random.random() - 0.5}"
        )
        return self.channel_voltage[channel]

    async def get_channel_current_measured(self, channel):
        logging.warning(
            f"Simulated: Channel {channel} measured current redout: "
            f"{self.channel_current[channel] + random.random() - 0.5}"
        )
        return self.channel_current[channel]

    async def get_channel_on(self, channel):
        logging.warning(
            f"Simulated: Channel {channel} state redout: {self.channel_on[channel]}"
        )
        return self.channel_on[channel]

    async def get_temperature(self):
        logging.warning(f"Simulated: Temperature redout: {self.temperature}")
        return self.temperature

    async def reset(self):
        self.channel_voltage = 8 * [None]
        self.channel_on = 8 * [None]
        logging.warning("Simulated: Resetting settings")
