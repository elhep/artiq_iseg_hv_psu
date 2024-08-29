#!/usr/bin/env python3

import abc
import asyncio
import logging
import socket


class ArtiqIsegHvPsuInterface(abc.ABC):
    @abc.abstractmethod
    async def set_channel_voltage(self, channel, voltage):
        pass

    @abc.abstractmethod
    async def get_channel_voltage(self, channel):
        pass

    @abc.abstractmethod
    async def set_channel_on(self, channel, channel_on):
        pass

    @abc.abstractmethod
    async def get_channel_on(self, channel):
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

    async def set_channel_on(self, channel, channel_on):
        if channel_on:
            self.send_command(f":VOLT ON,(@{channel})")
        else:
            self.send_command(f":VOLT OFF,(@{channel})")

    async def get_channel_voltage(self, channel):
        return self.send_command(f":READ:VOLT?(@{channel})")

    async def get_channel_on(self, channel):
        channel_status = self.send_command(f":READ:CHAN:STAT? (@{channel})")
        channel_on = bool(int(channel_status) & (1 << 3))
        return channel_on 

    async def reset(self):
        return self.send_command("*RST")

    def close(self):
        self.client.close()


class ArtiqIsegHvPsuSim(ArtiqIsegHvPsuInterface):
    def __init__(self):
        self.channel_voltage = 8 * [None]
        self.channel_on = 8 * [None]

    async def set_channel_voltage(self, channel, voltage):
        self.channel_voltage[channel] = voltage 
        logging.warning(f"Simulated: Setting channel {channel} voltage to {voltage}")

    async def set_channel_on(self, channel, channel_on):
        self.channel_on[channel] = channel_on
        if channel_on:
            logging.warning("Simulated: Turning channel {channel} ON")
        else:
            logging.warning("Simulated: Turning channel {channel } OFF")

    async def get_channel_voltage(self, channel):
        logging.warning(f"Simulated: Channel {channel} voltage redout: {self.channel_voltage[channel]}")
        return self.channel_voltage[channel]

    async def get_channel_on(self, channel):
        logging.warning(f"Simulated: Channel {channel} state redout: {self.channel_on[channel]}")
        return self.channel_on[channel]

    async def reset(self):
        self.channel_voltage = 8 * [None]
        self.channel_on = 8 * [None]
        logging.warning("Simulated: Resetting settings")
