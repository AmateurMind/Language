# campus_faq.py
# FAQ data structure for campus information

CAMPUS_FAQ = {
    "fees": {
        "en": {
            "questions": ["fee deadlines", "fee payment", "fee structure", "late fees", "payment methods"],
            "answers": "Fee deadlines vary by semester. Generally, fees are due within 30 days of semester start. Late payments incur a penalty of ₹500 per week. Payment methods include online banking, UPI, and demand draft. Contact the accounts office for specific deadlines."
        },
        "hi": {
            "questions": ["शुल्क की समय-सीमाएं", "शुल्क भुगतान", "शुल्क संरचना", "विलंब शुल्क", "भुगतान विधियां"],
            "answers": "शुल्क की समय-सीमाएं सेमेस्टर के अनुसार अलग-अलग होती हैं। आमतौर पर, सेमेस्टर शुरू होने के 30 दिनों के भीतर शुल्क जमा करना होता है। विलंब भुगतान पर प्रति सप्ताह ₹500 का जुर्माना लगता है। भुगतान के तरीकों में ऑनलाइन बैंकिंग, UPI और डिमांड ड्राफ्ट शामिल हैं। विशिष्ट समय-सीमाओं के लिए लेखा कार्यालय से संपर्क करें।"
        },
        "mr": {
            "questions": ["फी मुदती", "फी पेमेंट", "फी स्ट्रक्चर", "उशीरा फी", "पेमेंट पद्धती"],
            "answers": "फी मुदती सेमेस्टरनुसार बदलतात. सहसा, सेमेस्टर सुरू झाल्यापासून 30 दिवसांच्या आत फी भरावी लागते. उशीरा पेमेंटवर प्रति आठवड्याला ₹500 दंड आकारला जातो. पेमेंट पद्धतींमध्ये ऑनलाइन बँकिंग, UPI आणि डिमांड ड्राफ्ट यांचा समावेश होतो. विशिष्ट मुदतींसाठी अकाउंट्स ऑफिसशी संपर्क साधा."
        }
    },
    "scholarships": {
        "en": {
            "questions": ["scholarships", "financial aid", "merit scholarship", "need based scholarship"],
            "answers": "Various scholarships are available including merit-based, need-based, and category-based scholarships. Application deadlines are typically in July-August for odd semester and December-January for even semester. Required documents include mark sheets, income certificate, and bank details."
        },
        "hi": {
            "questions": ["छात्रवृत्ति", "वित्तीय सहायता", "मेरिट छात्रवृत्ति", "जरूरत आधारित छात्रवृत्ति"],
            "answers": "मेरिट-आधारित, जरूरत-आधारित और श्रेणी-आधारित सहित विभिन्न छात्रवृत्तियां उपलब्ध हैं। आवेदन की समय-सीमाएं आमतौर पर विषम सेमेस्टर के लिए जुलाई-अगस्त और सम सेमेस्टर के लिए दिसंबर-जनवरी में होती हैं। आवश्यक दस्तावेजों में मार्क शीट, आय प्रमाण पत्र और बैंक विवरण शामिल हैं।"
        },
        "mr": {
            "questions": ["शिष्यवृत्ती", "आर्थिक मदत", "मेरिट शिष्यवृत्ती", "गरज आधारित शिष्यवृत्ती"],
            "answers": "मेरिट-आधारित, गरज-आधारित आणि श्रेणी-आधारित शिष्यवृत्तींसह विविध शिष्यवृत्ती उपलब्ध आहेत. अर्जाची मुदत सहसा विषम सेमेस्टरसाठी जुलै-ऑगस्ट आणि सम सेमेस्टरसाठी डिसेंबर-जानेवारी असते. आवश्यक कागदपत्रांमध्ये मार्क शीट, उत्पन्न प्रमाणपत्र आणि बँक तपशील यांचा समावेश होतो."
        }
    },
    "timetable": {
        "en": {
            "questions": ["timetable", "class schedule", "lecture timings", "room changes"],
            "answers": "Timetables are available on the student portal and notice boards. Regular classes run from 9 AM to 5 PM. Any changes are notified through the college app and email. Check the academic section for the latest updates."
        },
        "hi": {
            "questions": ["समय-सारणी", "कक्षा अनुसूची", "व्याख्यान समय", "कक्ष परिवर्तन"],
            "answers": "समय-सारणियां छात्र पोर्टल और सूचना बोर्ड पर उपलब्ध हैं। नियमित कक्षाएं सुबह 9 बजे से शाम 5 बजे तक चलती हैं। कोई भी बदलाव कॉलेज ऐप और ईमेल के माध्यम से सूचित किया जाता है। नवीनतम अपडेट के लिए अकादमिक अनुभाग देखें।"
        },
        "mr": {
            "questions": ["वेळापत्रक", "वर्ग वेळापत्रक", "लेक्चर वेळा", "रूम बदल"],
            "answers": "वेळापत्रकं स्टुडंट पोर्टल आणि नोटिस बोर्डवर उपलब्ध आहेत. नियमित क्लास 9 AM ते 5 PM पर्यंत चालतात. कोणतेही बदल कॉलेज अॅप आणि ईमेलद्वारे कळवले जातात. नवीनतम अपडेटसाठी अकॅडमिक सेक्शन तपासा."
        }
    },
    "library": {
        "en": {
            "questions": ["library hours", "library services", "book issue", "library membership"],
            "answers": "Library hours: 8 AM to 8 PM (weekdays), 9 AM to 5 PM (weekends). Services include book lending, reference section, digital resources, and study spaces. Students need valid ID for membership and can issue up to 3 books for 14 days."
        },
        "hi": {
            "questions": ["पुस्तकालय समय", "पुस्तकालय सेवाएं", "किताब जारी करना", "पुस्तकालय सदस्यता"],
            "answers": "पुस्तकालय समय: सुबह 8 बजे से शाम 8 बजे (कार्यदिवस), सुबह 9 बजे से शाम 5 बजे (सप्ताहांत)। सेवाओं में किताब उधार, संदर्भ अनुभाग, डिजिटल संसाधन और अध्ययन स्थान शामिल हैं। सदस्यता के लिए वैध ID की आवश्यकता होती है और 14 दिनों के लिए 3 किताबें जारी की जा सकती हैं।"
        },
        "mr": {
            "questions": ["ग्रंथालय वेळा", "ग्रंथालय सेवा", "पुस्तक जारी", "ग्रंथालय सदस्यत्व"],
            "answers": "ग्रंथालय वेळा: 8 AM ते 8 PM (कार्यदिवस), 9 AM ते 5 PM (सप्ताहांत). सेवामध्ये पुस्तक कर्ज, संदर्भ विभाग, डिजिटल संसाधने आणि अभ्यास जागा यांचा समावेश होतो. सदस्यत्वासाठी वैध ID आवश्यक आहे आणि 14 दिवसांसाठी 3 पुस्तके काढता येतात."
        }
    }
}

def get_faq_response(query, language="en"):
    """
    Get FAQ response based on query and language
    """
    query_lower = query.lower()

    for category, lang_data in CAMPUS_FAQ.items():
        if language in lang_data:
            category_data = lang_data[language]

            # Check if query matches any question in this category
            for question in category_data["questions"]:
                if question.lower() in query_lower:
                    return category_data["answers"]

    return None