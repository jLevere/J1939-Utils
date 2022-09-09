from bitarray import bitarray
from bitarray.util import ba2hex, int2ba, ba2int


class J1939ID():
    """J1939 PDU ID

    CBFF and CEFF messages are both handled.  CBFF only has a priority and a source address field.

    J1939 is comprised of two CAN messages types:
        - CEFF messages are required by J1939 spec and defined in J1939-21
        - CBFF (Classical Base Frame Format) messages are generally proprietary and also defined in J1939-21

    The overall PDU should be described as hex but all the fields as ints.
    """

    def __init__(self, can_id: str = None, cbff: bool = False):
        self._cbff = cbff

        if not can_id:
            if cbff:
                self._can_id = bitarray(11)
                self._can_id[:] = False
            else:
                self._can_id = bitarray(29)
                self._can_id[:] = False  # set all to 0
        else:
            if int(can_id, 16) > 0x1fffffff:  # make sure incoming data isn't longer than 29 bits
                raise ValueError(
                    f"can_id: {can_id}, data must be 29bits or less")

            # this is a CBFF message ID with an 11bit can_id
            if len(can_id) <= 4 and int(can_id, 16) <= 0x7ff:
                self._cbff = True
                self._can_id = int2ba(int(can_id, 16), 11)
            else:
                self._can_id = int2ba(int(can_id, 16), 29)

    @property
    def can_id(self) -> str:
        """return canid as hex string

        Returns:
            str: hex string
        """
        return self.hex

    @can_id.setter
    def can_id(self, value: str) -> None:
        """set can id from hex string

        Args:
            value (str): hex string

        Raises:
            ValueError: canid is to large
        """
        if value[:2] == '0x':  # make sure that 0x doesn't mess it up
            value = value[2:]

        if len(value) > 8:  # if something is grossly wrong reject it
            raise ValueError(
                f"{value} is not valid canid, too long with len: {len(value)}")

        if self._cbff:
            self._can_id = int2ba(int(value, 16), 11)
        else:
            self._can_id = int2ba(int(value, 16), 29)

    @property
    def priority(self) -> int:
        """returns int priority.

        Returns:
            int: priority
        """
        return int((self._can_id[:3]).to01(), 2)

    @priority.setter
    def priority(self, value: int) -> None:
        """set priority from int value

        Args:
            value (int): priority
        """
        self._can_id[:3] = int2ba(value, length=3)

    @property
    def edp(self) -> int:
        """returns extended data page as int

        Returns:
            int: extended data page
        """
        if not self._cbff:
            return int((self._can_id[3:4]).to01(), 2)

    @edp.setter
    def edp(self, value: int) -> None:
        """set extended data page from int

        Args:
            value (int): extended data page
        """
        if not self._cbff:
            self._can_id[3:4] = int2ba(value, 1)

    @property
    def dp(self) -> int:
        """return data page as int

        Returns:
            int: data page
        """
        if not self._cbff:
            return int((self._can_id[4:5]).to01(), 2)

    @dp.setter
    def dp(self, value: int) -> None:
        """set data page from int

        Args:
            value (int): data page
        """
        if not self._cbff:
            self._can_id[4:5] = int2ba(value, 1)

    @property
    def pf(self) -> int:
        """return protocol data unit format (pdu format) as int

        Returns:
            int: pdu format
        """
        if not self._cbff:
            return int((self._can_id[5:13]).to01(), 2)

    @pf.setter
    def pf(self, value: int) -> None:
        """set pdu format from int

        Args:
            value (int): pdu format
        """
        if not self._cbff:
            self._can_id[5:13] = int2ba(value, 8)

    @property
    def ps(self) -> int:
        """return pdu specific as int

        Returns:
            int: pdu specific
        """
        if not self._cbff:
            return ba2int(self._can_id[13:21])

    @ps.setter
    def ps(self, value: int) -> None:
        """set protocol data unit specific (pdu specific) from int

        Args:
            value (int): pdu specific
        """
        if not self._cbff:
            self._can_id[13:21] = int2ba(value, 8)

    @property
    def sa(self) -> int:
        """return source address as int

        Returns:
            int: source address
        """
        if not self._cbff:
            return int((self._can_id[21:29]).to01(), 2)
        else:  # is cbff
            return int((self._can_id[3:11].to01()), 2)

    @sa.setter
    def sa(self, value: int) -> None:
        """set source address from int

        Args:
            value (int): _description_
        """
        if not self._cbff:
            self._can_id[21:29] = int2ba(value, 8)
        else:  # is cbff
            self._can_id[3:11] = int2ba(value, 8)

    @property
    def da(self) -> int:
        """return destination address as int.
        if type 1, return ps
        if type 2, return global da 255

        Returns:
            int: destination
        """
        if not self._cbff:
            if self.type == 1:
                return self.ps
            else:
                return int("0xFF", 16)

    @da.setter
    def da(self, value: int) -> None:
        """set the destination address from int.

        If PDU is type 2 then the dest addr is understood to be global and the field is used to identify the pgn.
        So, if you change it you will alter the PGN.  Method will not stop you but will print a warning.

        Args:
            value (int): destination address
        """
        if not self._cbff:
            if self.type == 1:
                self.ps = value
            else:
                print(
                    f"WARN: {__class__} setting the dest address when in pdu type 2 will alter the PGN. Contenuing anyway.")
                self.ps = value

    @property
    def pgn(self) -> int:
        """return parameter group number as int

        Returns:
            int: parameter group number
        """
        # 6*b'0' + edp, dp, pf + if pf < 240: + 8d'0' else + ps
        if not self._cbff:
            pgn_bits = bitarray(24)
            pgn_bits[:] = False  # set all to 0
            pgn_bits[6:7] = int2ba(self.edp, 1)
            pgn_bits[7:8] = int2ba(self.dp, 1)
            pgn_bits[8:16] = int2ba(self.pf, 8)

            if self.type == 1:
                blank_byte = bitarray(8)
                blank_byte[:] = False
                pgn_bits[16:24] = blank_byte
            else:
                pgn_bits[16:24] = int2ba(self.ps, 8)
            return ba2int(pgn_bits)

    @pgn.setter
    def pgn(self, value: int) -> None:
        """set pgn from int.
        This is actually just setting other fields.

        Args:
            value (int): pgn value
        """
        if not self._cbff:
            pgn_bits = int2ba(value, 24)
            self._can_id[3:4] = pgn_bits[6:7]  # edp
            self._can_id[4:5] = pgn_bits[7:8]  # dp
            self._can_id[5:13] = pgn_bits[8:16]  # pf
            self._can_id[13:21] = pgn_bits[16:24]  # ps

    ################# utilities #############################

    @property
    def dict(self) -> dict:
        """returns dict containing all the values of the PDU as ints

        Returns:
            dict: pdu as dict
        """
        rep = {
            "can_id": self.can_id,
            "priority": self.priority,
            "edp": self.edp,
            "dp": self.dp,
            "pf": self.pf,
            "ps": self.ps,
            "sa": self.sa,
            "da": self.da,
            "pgn": self.pgn,
            "pdu_type": self.type,
        }

        if self._cbff:
            rep['id_type'] = "cbff"
        return rep

    @property
    def bin(self) -> str:
        """returns binary version of the j1939 can id

        Returns:
            str: string of bits
        """
        return self._can_id.to01()

    @property
    def hex(self) -> str:
        """returns the hex value of the can id.
        j1939 can ids are only 29bits long, so
        it is filled with 0s to an even number of bytes

        Returns:
            str: hex representation of j1939 can id
        """
        filled = self._can_id.copy()
        filled.reverse()
        filled.fill()
        filled.reverse()

        return (ba2hex(filled)).upper()

    @property
    def bitarray(self) -> bitarray:
        """returns the bitarray object of the j1939 can id.
        This is helpful if you want to do more customization of the
        can id or inspect its object.

        Returns:
            bitarray: bitarray object holding the can id
        """
        return self._can_id

    @property
    def type(self) -> int:
        """returns the protocol data unit type as int

        Returns:
            int: protocol data unit type
        """
        if not self._cbff:
            if self.pf < 240:
                return 1
            else:
                return 2

    @property
    def cbff(self) -> bool:
        """returns if current object is cbff type message

        Returns:
            bool: true if cbff
        """
        return self._cbff

    ####################### builtins ##########################

    def __repr__(self) -> str:
        return str(self.hex)

    def __str__(self) -> str:
        if not self._cbff:
            return "{}    {:02d} {:05d} {:02d} --> {:02d}".format(self.hex, self.priority, self.pgn,
                                                                  self.sa, self.da)
        else:
            return "{}    {:02d} cbff {:02d} --> None".format(self.hex, self.priority, self.sa)
