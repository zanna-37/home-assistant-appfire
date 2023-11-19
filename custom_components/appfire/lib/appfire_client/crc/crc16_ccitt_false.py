class Crc16_ccitt_false:
    @staticmethod
    def crc_from(data: bytes) -> hex:
        # https://gist.github.com/tijnkooijmans/10981093?permalink_comment_id=2898199#gistcomment-2898199

        poly = 0x1021
        crc = 0xFFFF

        for i in range(0, len(data)):
            crc ^= data[i] << 8
            for j in range(0, 8):
                if (crc & 0x8000) > 0:
                    crc = (crc << 1) ^ poly
                else:
                    crc = crc << 1

        return crc & 0xFFFF
