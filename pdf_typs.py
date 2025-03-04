import functools
import unicodedata

def handle_split_index(text, index):
    parts = text.split('\n')
    if len(parts) > index:
        return unicodedata.normalize('NFKC', parts[index])
    else:
        return None
def handle_replace_newline(text):
    return unicodedata.normalize('NFKC', text.replace('\n', ''))

def handle_reading_type(text):
    out_text = text.replace('\n', '')
    raTy = out_text.split("-")
    if len(raTy) > 1:
        return f"{raTy[0]} - {unicodedata.normalize('NFKC', raTy[1])}"
    else:
        raTy = out_text.split(" ")
        if len(raTy) > 1:
            return f"{raTy[0]} - {unicodedata.normalize('NFKC', raTy[1])}"
        else:
            return unicodedata.normalize('NFKC', out_text)
pdf_types = {
    'new_nama': {
    'fields': {
        'Customer': {
            'coordinates': (251.00799560546875, 126.00079345703125, 529.9940185546875, 152.98681640625),
            'handler': handle_replace_newline,
        },
        'Customer_No': {
            'coordinates': (25.96500015258789, 152.957763671875, 115.96499633789062, 170.957763671875),
            'handler': handle_replace_newline,
        },
        'Account_No': {
            'coordinates': (25.96500015258789, 126.00079345703125, 115.96499633789062, 152.98681640625),
            'handler': handle_replace_newline,
        },
        'Meter_No': {
            'coordinates': (511.9649963378906, 242.957763671875, 574.97998046875, 269.9727783203125),
            'handler': functools.partial(handle_split_index, index=2),
        },
        'Previous_Reading_Date': {
            'coordinates': (403.9649963378906, 251.9727783203125, 457.9649963378906, 269.9727783203125),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Previous_Reading': {
            'coordinates': (403.9649963378906, 251.9727783203125, 457.9649963378906, 269.9727783203125),
            'handler': functools.partial(handle_split_index, index=1),
        },
        'Current_Reading_Date': {
            'coordinates': (468.3970031738281, 245.39581298828125, 504.3970031738281, 269.9727783203125),
            'handler': functools.partial(handle_split_index, index=1),
        },
        'Current_Reading': {
            'coordinates': (468.3970031738281, 245.39581298828125, 504.3970031738281, 269.9727783203125),
            'handler': functools.partial(handle_split_index, index=2),
        },
        'Due_Date': {
            'coordinates': (25.96500015258789, 62.98681640625, 88.9800033569336, 98.98681640625),
            'handler': handle_replace_newline,
        },
        'Reading_Type': {
            'coordinates': (403.9649963378906, 324.00079345703125, 493.9649963378906, 350.9867858886719),
            'handler': handle_replace_newline,
        },
        'Tariff_Type': {
            'coordinates': (25.96500015258789, 170.957763671875, 115.96499633789062, 188.957763671875),
            'handler': handle_replace_newline,
        },
        'Invoice_Month': {
            'coordinates': (241.96499633789062, 62.476806640625, 304.9800109863281, 98.957763671875),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Government_Subsidy': {
            'coordinates': (25.96500015258789, 450.00079345703125, 88.9800033569336, 476.9867858886719),
            'handler': handle_replace_newline,
        },
        'Consumption_KWH_1': {
            'coordinates': (303.5802001953125, 256.51824951171875, 335.5885925292969, 262.11968994140625),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_1': {
            'coordinates': (229.8000030517578, 257.7000732421875, 249.8499755859375, 262.300048828125),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_2': {
            'coordinates': (303.34161376953125, 266.28216552734375, 335.3499755859375, 270.72198486328125),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_2': {
            'coordinates': (229.86520385742188, 266.0653076171875, 249.91517639160156, 270.66522216796875),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_3': {
            'coordinates': (303.3030090332031, 274.645751953125, 335.3113708496094, 279.08551025390625),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_3': {
            'coordinates': (229.930419921875, 274.23040771484375, 249.98045349121094, 278.83038330078125),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_4': {
            'coordinates': (303.264404296875, 283.00946044921875, 335.2726745605469, 287.44921875),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_4': {
            'coordinates': (230.09571838378906, 282.79571533203125, 250.14576721191406, 287.39569091796875),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_5': {
            'coordinates': (314.97320556640625, 291.368408203125, 333.91241455078125, 296.505615234375),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_5': {
            'coordinates': (230.2609100341797, 291.160888671875, 250.31094360351562, 295.7608642578125),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_6': {
            'coordinates': (314.9541015625, 299.9581298828125, 333.89337158203125, 305.09539794921875),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_6': {
            'coordinates': (230.22610473632812, 299.22613525390625, 250.2760772705078, 303.82611083984375),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Total_Before_VAT': {
            'coordinates': (268.9800109863281, 512.957763671875, 322.9800109863281, 530.957763671875),
            'handler': handle_replace_newline,
        },
        'VAT': {
            'coordinates': (259.9939880371094, 530.957763671875, 331.9939880371094, 548.957763671875),
            'handler': handle_replace_newline,
        },
        'Total_After_VAT': {
            'coordinates': (259.9939880371094, 548.957763671875, 331.9939880371094, 566.957763671875),
            'handler': handle_replace_newline,
        },
        'Total_Payable_Amount': {
            'coordinates': (259.9939880371094, 593.9727783203125, 331.9939880371094, 611.9727783203125),
            'handler': handle_replace_newline,
        },
    }
    },
    'old_nama': {
    'fields': {
        'Customer': {
            'coordinates': (323.63995361328125, 90.23686218261719, 422.37310791015625, 98.6377944946289),
            'handler': handle_replace_newline,
        },
        'Customer_No': {
            'coordinates': (52.43997573852539, 230.51683044433594, 86.9945068359375, 238.9177703857422),
            'handler': handle_replace_newline,
        },
        'Account_No': {
            'coordinates': (54.35997772216797, 209.51683044433594, 85.03715515136719, 217.9177703857422),
            'handler': handle_replace_newline,
        },
        'Meter_No': {
            'coordinates': (417.23980712890625, 227.15728759765625, 553.2330932617188, 238.95947265625),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Previous_Reading_Date': {
            'coordinates': (417.23980712890625, 227.15728759765625, 553.2330932617188, 238.95947265625),
            'handler': functools.partial(handle_split_index, index=2),
        },
        'Previous_Reading': {
            'coordinates': (417.23980712890625, 227.15728759765625, 553.2330932617188, 238.95947265625),
            'handler': functools.partial(handle_split_index, index=4),
        },
        'Current_Reading_Date': {
            'coordinates': (417.23980712890625, 227.15728759765625, 553.2330932617188, 238.95947265625),
            'handler': functools.partial(handle_split_index, index=1),
        },
        'Current_Reading': {
            'coordinates': (417.23980712890625, 227.15728759765625, 553.2330932617188, 238.95947265625),
            'handler': functools.partial(handle_split_index, index=3),
        },
        'Due_Date': {
            'coordinates': (52.43997573852539, 336.23681640625, 88.39714050292969, 344.63775634765625),
            'handler': handle_replace_newline,
        },
        'Reading_Type': {
            'coordinates': (432.23681640625, 307.79730224609375, 467.5762023925781, 315.03948974609375),
            'handler': handle_reading_type,
        },
        'Tariff_Type': {
            'coordinates': (30.719985961914062, 357.2377624511719, 110.00762939453125, 369.441162109375),
            'handler': handle_reading_type,
        },
        'Invoice_Month': {
            'coordinates': (34.677085876464844, 315.2373046875, 104.76636505126953, 322.4794921875),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Government_Subsidy': {
            'coordinates': (25.96500015258789, 458.9577941894531, 88.9800033569336, 485.9727783203125),
            'handler': handle_replace_newline,
        },
        'Consumption_KWH_1': {
                'coordinates': (301.56591796875, 234.96929931640625, 335.8042297363281, 239.814208984375),
                'handler': functools.partial(handle_split_index, index=0),
            },
        'Rate_1': {
            'coordinates': (227.30224609375, 235.45001220703125, 252.4168243408203, 240.28167724609375),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_2': {
            'coordinates': (301.596435546875, 243.661865234375, 335.8347473144531, 248.50677490234375),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_2': {
            'coordinates': (227.56048583984375, 244.79998779296875, 252.67506408691406, 248.70001220703125),
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_3': {
            'coordinates': (301.9205322265625, 252.06085205078125, 336.1588439941406, 256.1107177734375),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_3': {
            'coordinates': (227.56048583984375, 252.5289306640625, 252.67506408691406, 256.456298828125),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_4': {
            'coordinates': (301.51055908203125, 260.0194091796875, 335.7488708496094, 264.06927490234375),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_4': {
            'coordinates': (227.6121826171875, 260.48699951171875, 252.7267608642578, 264.20770263671875),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_5': {
            'coordinates': (0,0,0,0),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_5': {
            'coordinates': (0,0,0,0),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Consumption_KWH_6': {
            'coordinates': (0,0,0,0),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Rate_6': {
            'coordinates': (0,0,0,0),  # Update with actual coordinates if available
            'handler': functools.partial(handle_split_index, index=0),
        },
        'Total_Before_VAT': {
            'coordinates': (282.4798278808594, 503.3967590332031, 303.79693603515625, 511.7976989746094),
            'handler': handle_replace_newline,
        },
        'VAT': {
            'coordinates': (282.4798889160156, 522.956787109375, 303.7969970703125, 531.3577270507812),
            'handler': handle_replace_newline,
        },
        'Total_After_VAT': {
            'coordinates': (281.7602844238281, 544.6767578125, 303.077392578125, 553.0776977539062),
            'handler': handle_replace_newline,
        },
        'Total_Payable_Amount': {
            'coordinates': (281.27978515625, 585.9567260742188, 306.4368896484375, 594.357666015625),
            'handler': handle_replace_newline,
        },
    }
},
    'dofar':{
    'fields': {
        'Customer': {
            'coordinates': (111.8499984741211, 79.53300476074219, 567.740234375, 103.4900131225586),
            'handler': handle_replace_newline
        },
        'Customer_No': {
            'coordinates': (13.809629440307617, 239.3231201171875, 107.16871643066406, 258.22418212890625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Account_No': {
            'coordinates': (13.63270092010498, 214.48138427734375, 106.99183654785156, 233.38238525390625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Meter_No': {
            'coordinates': (548.78759765625, 231.98046875, 603.4139404296875, 265.37030029296875),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Previous_Reading_Date': {
            'coordinates': (426.49517822265625, 247.86566162109375, 481.91424560546875, 259.041015625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Previous_Reading': {
            'coordinates': (426.4488830566406, 232.33697509765625, 481.8679504394531, 243.5123291015625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Current_Reading_Date': {
            'coordinates': (488.64227294921875, 247.86199951171875, 544.0614013671875, 259.037353515625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Current_Reading': {
            'coordinates': (488.8852233886719, 231.7376708984375, 544.3042602539062, 242.91302490234375),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Due_Date': {
            'coordinates': (13.929361343383789, 362.3560791015625, 107.28851318359375, 381.257080078125),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Reading_Type': {
            'coordinates': (423.8912048339844, 339.1375732421875, 509.988037109375, 361.95849609375),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Tariff_Type': {
            'coordinates': (13.752420425415039, 388.48828125, 107.11151885986328, 407.3892822265625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Invoice_Month': {
            'coordinates': (489.27301025390625, 231.6158447265625, 543.237060546875, 265.1710205078125),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Government_Subsidy': {
            'coordinates': (8.956999778747559, 495.83599853515625, 98.95700073242188, 531.8359985351562),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Rate_1': {
            'coordinates': (315.1936340332031, 243.9964599609375, 341.1388244628906, 254.20111083984375),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Rate_2': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Rate_3': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Rate_4': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Rate_5': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Rate_6': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Consumption_KWH_1': {
            'coordinates': (350.4316101074219, 244.01959228515625, 375.3755187988281, 254.201171875),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Consumption_KWH_2': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Consumption_KWH_3': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Consumption_KWH_4': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Consumption_KWH_5': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Consumption_KWH_6': {
            'coordinates': (0, 0, 0, 0),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Total_Before_VAT': {
            'coordinates': (274.8828125, 384.6558837890625, 348.78997802734375, 413.267578125),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'VAT': {
            'coordinates': (274.789306640625, 422.73797607421875, 348.69647216796875, 451.34967041015625),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Total_After_VAT': {
            'coordinates': (273.900390625, 497.091064453125, 347.80755615234375, 525.7028198242188),
            'handler': functools.partial(handle_split_index, index=0)
        },
        'Total_Payable_Amount': {
            'coordinates': (279.5530090332031, 608.739990234375, 346.677001953125, 630.0280151367188),
            'handler': functools.partial(handle_split_index, index=0)
        }
    }
    }
}
