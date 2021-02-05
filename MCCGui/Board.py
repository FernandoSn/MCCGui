import mcculw
import ctypes

class Board():

    _SAMPLINGFR = (1000,2000,4000,6000,8000,10000,14000,20000,30000) #in Hz. Do not change!
    _VRANGE = (2, 5, 10) #±Volts. Do not change!

    isTTLON = False

    scan_options = mcculw.enums.ScanOptions.SCALEDATA | \
                   mcculw.enums.ScanOptions.CONVERTDATA | \
                   mcculw.enums.ScanOptions.BACKGROUND | \
                   mcculw.enums.ScanOptions.CONTINUOUS | \
                   mcculw.enums.ScanOptions.SINGLEIO

    def __init__(self, DeviceDescriptor, BoardNum, VRange, SRate,Channels):

        self.ProductName = DeviceDescriptor.product_name
        self.SerialNum =  DeviceDescriptor.unique_id
        self.BoardNum = BoardNum
        self.VRange = self.getVRangeFromUL(VRange)
        self.SRate = SRate
        self.Channels = Channels
        mcculw.ul.create_daq_device(BoardNum, DeviceDescriptor)

    def testBoard(self):

        #All vars created here are temp.

        mcculw.ul.a_input_mode(self.BoardNum, mcculw.enums.AnalogInputMode.SINGLE_ENDED)
        total_count = int(self.Channels  * (self.SRate / 10))
        scan_options = mcculw.enums.ScanOptions.SCALEDATA | \
                       mcculw.enums.ScanOptions.CONVERTDATA | \
                       mcculw.enums.ScanOptions.SINGLEIO
        memhandle = mcculw.ul.scaled_win_buf_alloc(total_count)
        mcculw.ul.a_in_scan(self.BoardNum, 0, self.Channels-1
                            , total_count, self.SRate,
                            self.VRange, memhandle, scan_options)
        mcculw.ul.win_buf_free(memhandle)


    def getVRangeFromUL(self,VRange):
        if VRange == 2:
            return mcculw.enums.ULRange.BIP2VOLTS

        elif VRange == 5:
            return mcculw.enums.ULRange.BIP5VOLTS

        else:
            return mcculw.enums.ULRange.BIP10VOLTS

    def run(self):
        self.total_count = int(self.Channels  * self.SRate * 2)
        self.memhandle = mcculw.ul.scaled_win_buf_alloc(self.total_count)
        self.PtrMemhandle = ctypes.cast(self.memhandle, ctypes.POINTER(ctypes.c_double))
        mcculw.ul.a_in_scan(self.BoardNum, 0, self.Channels - 1
                            , self.total_count, self.SRate,
                            self.VRange, self.memhandle, self.scan_options)


    def stop(self):
        mcculw.ul.stop_background(self.BoardNum, mcculw.enums.FunctionType.AIFUNCTION)
        mcculw.ul.win_buf_free(self.memhandle)

    def ReleaseBoard(self):
        mcculw.ul.release_daq_device(self.BoardNum)

    def getStatus(self):
        status, curr_count, curr_index = mcculw.ul.get_status(self.BoardNum, mcculw.enums.FunctionType.AIFUNCTION)
        return status, curr_index, curr_count

    def ConfigDigitalPort(self):
        mcculw.ul.d_config_port(self.BoardNum, mcculw.enums.DigitalPortType.AUXPORT, mcculw.enums.DigitalIODirection.OUT)

    def TTLON(self):
        mcculw.ul.d_out(self.BoardNum, mcculw.enums.DigitalPortType.AUXPORT, 1)
        return True

    def TTLOFF(self):
        mcculw.ul.d_out(self.BoardNum, mcculw.enums.DigitalPortType.AUXPORT, 0)
        return False

    def TTLSwitch(self):
        if self.isTTLON:
            self.isTTLON = self.TTLOFF()
        else:
            self.isTTLON = self.TTLON()