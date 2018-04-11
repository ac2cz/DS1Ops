#!/usr/bin/env python3

# Copyright (c) 2013, Eduard Broecker
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that
# the following conditions are met:
#
#    Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

from __future__ import print_function
from __future__ import absolute_import

# from .log import setup_logger, set_log_level
#logger = setup_logger('root')
import sys
import os
sys.path.append('..')
import canmatrix.formats
import canmatrix.canmatrix as cm
import canmatrix.copy as cmcp


def toPyObject(infile, outfileName, **options):
    dbs = {}

    #logger.info("Importing " + infile + " ... ")
    dbs = canmatrix.formats.loadp(infile, **options)
    #logger.info("done\n")

    #logger.info("Exporting " + outfileName + " ... ")

    outdbs = {}
    for name in dbs:
        db = None

        if 'ecus' in options and options['ecus'] is not None:
            ecuList = options['ecus'].split(',')
            db = cm.CanMatrix()
            for ecu in ecuList:
                #logger.info("Copying ECU " + ecu)
                cmcp.copyBUwithFrames(ecu, dbs[name], db)
        if 'frames' in options and options['frames'] is not None:
            frameList = options['frames'].split(',')
            db = cm.CanMatrix()
            for frame in frameList:
                #logger.info("Copying Frame " + frame)
                cmcp.copyFrame(frame, dbs[name], db)
        if db is None:
            db = dbs[name]

        if 'merge' in options and options['merge'] is not None:
            mergeFiles = options['merge'].split(',')
            for database in mergeFiles:
                mergeString = database.split(':')
                dbTempList = canmatrix.formats.loadp(mergeString[0])
                for dbTemp in dbTempList:
                    if mergeString.__len__() == 1:
                        print ("merge complete: " + mergeString[0])
                        for frame in dbTempList[dbTemp].frames:
                            cmcp.copyFrame(frame.id, dbTempList[dbTemp], db)
                    for mergeOpt in mergeString[1:]:
                        if mergeOpt.split('=')[0] == "ecu":
                            cmcp.copyBUwithFrames(
                                mergeOpt.split('=')[1], dbTempList[dbTemp], db)
                        if mergeOpt.split('=')[0] == "frame":
                            cmcp.copyFrame(
                                mergeOpt.split('=')[1], dbTempList[dbTemp], db)

        if 'renameEcu' in options and options['renameEcu'] is not None:
            renameTuples = options['renameEcu'].split(',')
            for renameTuple in renameTuples:
                old, new = renameTuple.split(':')
                db.renameEcu(old, new)
        if 'deleteEcu' in options and options['deleteEcu'] is not None:
            deleteEcuList = options['deleteEcu'].split(',')
            for ecu in deleteEcuList:
                db.delEcu(ecu)
        if 'renameFrame' in options and options['renameFrame'] is not None:
            renameTuples = options['renameFrame'].split(',')
            for renameTuple in renameTuples:
                old, new = renameTuple.split(':')
                db.renameFrame(old, new)
        if 'deleteFrame' in options and options['deleteFrame'] is not None:
            deleteFrameList = options['deleteFrame'].split(',')
            for frame in deleteFrameList:
                db.delFrame(frame)
        if 'renameSignal' in options and options['renameSignal'] is not None:
            renameTuples = options['renameSignal'].split(',')
            for renameTuple in renameTuples:
                old, new = renameTuple.split(':')
                db.renameSignal(old, new)
        if 'deleteSignal' in options and options['deleteSignal'] is not None:
            deleteSignalList = options['deleteSignal'].split(',')
            for signal in deleteSignalList:
                db.delSignal(signal)

        if 'deleteZeroSignals' in options and options['deleteZeroSignals']:
            db.deleteZeroSignals()

        if 'deleteSignalAttributes' in options and options[
                'deleteSignalAttributes']:
            unwantedAttributes = options['deleteSignalAttributes'].split(',')
            db.delSignalAttributes(unwantedAttributes)

        if 'deleteFrameAttributes' in options and options[
                'deleteFrameAttributes']:
            unwantedAttributes = options['deleteFrameAttributes'].split(',')
            db.delFrameAttributes(unwantedAttributes)

        if 'deleteObsoleteDefines' in options and options[
                'deleteObsoleteDefines']:
            db.deleteObsoleteDefines()

        if 'recalcDLC' in options and options['recalcDLC']:
            db.recalcDLC(options['recalcDLC'])

        #logger.info(name)
        #logger.info("%d Frames found" % (db.frames.__len__()))

        outdbs[name] = db

    #print(outdbs[''].frames._list[0]._name)
    return outdbs['']
'''
def createCHeader(candb, cFileName):
    #print(candb.frames._list[0]._name)
    cFile = open(cFileName, "w")
    cFile.write("#ifndef CANDB_HEADER\n#define CANDB_HEADER\n\n")
    cFile.write("#include <stdint.h>\n\n")
    for frame in candb.frames:
        cFile.write("typedef struct {\n")
        for sig in frame:
            if sig.is_signed:
                cFile.write("\tint")
            else:
                cFile.write("\tuint")
            if sig.signalsize == 8:
                cFile.write("8_t ")
            elif sig.signalsize == 16:
                cFile.write("16_t ")
            elif sig.signalsize == 32:
                cFile.write("32_t ")
            else:
                cFile.write("64_t ")
            cFile.write(sig.name + ";\n")
        cFile.write("} " + frame.name + ";\n\n")
    cFile.write("\n#endif")
    cFile.close()'''

def tlmGetType(signal):
    if (signal.is_float):
        return "FLOAT"
    elif (signal.is_signed):
        return "INT"
    else:
        return "UINT"

def createCosmosTlm(candb, tlmFileName):
    tlmFile = open(tlmFileName, "w")
    tlm_id = 0;
    for frame in candb.frames:
        tlmFile.write("TELEMETRY CAN_LOCAL {} BIG_ENDIAN \n".format(frame.name))
        tlmFile.write("\tAPPEND_ITEM LENGTH 16 UINT \"Length of TCP-ized CAN message (always 36/0x24 bytes) \" \n ")
        tlmFile.write("\tAPPEND_ID_ITEM FIXED_TYPE 16 UINT 128 \"Fixed message type for CAN\" BIG_ENDIAN\n")
        tlmFile.write("\tAPPEND_ITEM TAG 64 UINT \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
        tlmFile.write("\tAPPEND_ITEM TIMESTAMP_L 32 UINT \"Timestamp of the CAN message, in microseconds.  This is the lower 4 bytes of the timestamp.\"\n")
        tlmFile.write("\tAPPEND_ITEM TIMESTAMP_H 32 UINT \"Timestamp of the CAN message, in microseconds.  This is the upper 4 bytes of the timestamp.\"\n")
        tlmFile.write("\tAPPEND_ITEM CHANNEL 8 UINT \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
        tlmFile.write("\tAPPEND_ITEM DLC 8 UINT \"Date Length Count from the CAN message.\"\n")
        tlmFile.write("\tAPPEND_ITEM FLAGS 16 UINT \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
        tlmFile.write("\tAPPEND_ITEM CANID_PADDING 1 UINT \"Fixed value of 0 - reserved.\"\n")
        tlmFile.write("\tAPPEND_ITEM CANID_RTR 1 UINT \"RTR value.\"\n")
        tlmFile.write("\tAPPEND_ITEM CANID_TYPE 1 UINT \"Indicates whether the message is a standard or extended frame.\"\n")
        tlmFile.write("\tAPPEND_ID_ITEM CANID_ID 29 UINT {} \"The ID (normal or extended) portion of the 'CAN ID' set of headers.\"\n".format(frame.id))
        tlmFile.write("\t\tSTATE EXTENDED 1\n")
        tlmFile.write("\t\tSTATE STANDARD 0\n")
        signal_size = 0
        for signal in frame:
            signal_size = signal_size + signal.signalsize
            signalType = tlmGetType(signal)
            if signal.is_little_endian and False:
                signalEndian = "LITTLE_ENDIAN"
            else:
                signalEndian = "BIG_ENDIAN"
            tlmFile.write("\tAPPEND_ITEM {} {} {} \"{}\" {}\n".format(signal.name,
                                                            signal.signalsize,
                                                            signalType,
                                                            signal.comment,
                                                            signalEndian))
        if signal_size != 64:
            tlmFile.write("\tAPPEND_ITEM PADDING {} UINT \"Padded bits for CAN data\"\n\n".format(64 - signal_size))
def createCosmosCmd(candb, tlmFileName):
    tlmFile = open(tlmFileName, "w")
    tlm_id = 0;
    for frame in candb.frames:
        tlmFile.write("COMMAND CAN_LOCAL_CMD {} BIG_ENDIAN \n".format(frame.name))
        tlmFile.write("\tAPPEND_PARAMETER LENGTH 16 UINT MIN MAX  36 \"Length of TCP-ized CAN message (always 36/0x24 bytes) \" \n ")
        tlmFile.write("\t\tSTATE DEFAULT 36 \n")
        tlmFile.write("\tAPPEND_ID_PARAMETER FIXED_TYPE 16 UINT MIN MAX  128 \"Fixed message type for CAN\" BIG_ENDIAN\n")
        tlmFile.write("\t\tSTATE DEFAULT 128 \n")
        tlmFile.write("\tAPPEND_PARAMETER TAG 64 UINT MIN MAX  0 \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 0 \n")
        tlmFile.write("\tAPPEND_PARAMETER TIMESTAMP_L 32 UINT MIN MAX  0 \"Timestamp of the CAN message, in microseconds.  This is the lower 4 bytes of the timestamp.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 0 \n")
        tlmFile.write("\tAPPEND_PARAMETER TIMESTAMP_H 32 UINT MIN MAX  0 \"Timestamp of the CAN message, in microseconds.  This is the upper 4 bytes of the timestamp.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 0 \n")
        tlmFile.write("\tAPPEND_PARAMETER CHANNEL 8 UINT MIN MAX  0  \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 0 \n")
        tlmFile.write("\tAPPEND_PARAMETER DLC 8 UINT MIN MAX  8  \"Date Length Count from the CAN message.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 8 \n")
        tlmFile.write("\tAPPEND_PARAMETER FLAGS 16 UINT MIN MAX  2 \"NOT USED in current PCAN-Ethernet Gateway DR hardware/software.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 2 \n")
        tlmFile.write("\tAPPEND_PARAMETER CANID_PADDING 1 UINT MIN MAX  0 \"Fixed value of 0 - reserved.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 0 \n")
        tlmFile.write("\tAPPEND_PARAMETER CANID_RTR 1 UINT MIN MAX  0 \"RTR value.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 0 \n")
        tlmFile.write("\tAPPEND_PARAMETER CANID_TYPE 1 UINT MIN MAX  1  \"Indicates whether the message is a standard or extended frame.\"\n")
        tlmFile.write("\t\tSTATE DEFAULT 1 \n")
        tlmFile.write("\tAPPEND_PARAMETER CANID_ID 29 UINT MIN MAX  {} \"The ID (normal or extended) portion of the 'CAN ID' set of headers.\"\n".format(frame.id))
        tlmFile.write("\t\tSTATE DEFAULT {} \n".format(frame.id))
        signal_size = 0
        for signal in frame:
            signal_size = signal_size + signal.signalsize
            signalType = tlmGetType(signal)
            if signal.is_little_endian and False:
                signalEndian = "LITTLE_ENDIAN"
            else:
                signalEndian = "BIG_ENDIAN"
            tlmFile.write("\tAPPEND_PARAMETER {} {} {} MIN MAX  0 \"{}\" {}\n".format(signal.name,
                                                            signal.signalsize,
                                                            signalType,
                                                            signal.comment,
                                                            signalEndian))
        if signal_size != 64:
            tlmFile.write("\tAPPEND_PARAMETER PADDING {} UINT MIN MAX 0 \"Padded bits for CAN data\"\n\n".format(64 - signal_size))

def main():
    from optparse import OptionParser

    usage = """
    %prog [options] import-file export-file

    import-file: *.dbc|*.dbf|*.kcd|*.arxml|*.json|*.xls(x)|*.sym
    export-file: *.dbc|*.dbf|*.kcd|*.arxml|*.json|*.xls(x)|*.sym

    followig formats are availible at this installation:
    \n"""

    for suppFormat, features in canmatrix.formats.supportedFormats.items():
        usage += suppFormat + "\t"
        if 'load' in features:
            usage += "import"
        usage += "\t"
        if 'dump' in features:
            usage += "export"
        usage += "\n"

    parser = OptionParser(usage=usage)

    (cmdlineOptions, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    infile = args[0]
    outfileName = args[1]

    CANObj = toPyObject(infile, outfileName, **cmdlineOptions.__dict__)

    createCosmosCmd(CANObj, "cmd.txt")
    createCosmosTlm(CANObj, "tlm.txt")


if __name__ == '__main__':
    sys.exit(main())