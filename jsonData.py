### jsonData -- Contanins json variables commonly used 
###             in the bomTool to communicate with the 
###             google sheets api

class jsonData: 
    def __init__(self):

        # RGB Gray Constants
        lightGray = 239 
        darkGray = 204
        tableBorderGray = 220

        # Table Colors
        self.lightColor = {
                         "backgroundColorStyle": {
                            "rgbColor": {
                                "red": 256 - lightGray,
                                "green": 256 - lightGray,
                                "blue": 256 - lightGray,
                             }
                          }
                       }
        self.darkColor = {
                        "backgroundColorStyle": {
                            "rgbColor": {
                                "red": 256 - darkGray,
                                "green": 256 - darkGray,
                                "blue": 256 - darkGray
                             }
                          }
                     }

        # Default Format for resetting formatting
        self.defaultFormat = {  
                            "backgroundColor": {
                                "red": 1 ,
                                "green": 1,
                                "blue": 1 
                            },

                            "borders": {
                                "top": {
                                    "style": "SOLID", 
                                    "color": {
                                        "red": 256 - tableBorderGray,
                                        "green": 256 - tableBorderGray,
                                        "blue": 256 - tableBorderGray
                                    }
                                 },
                                "bottom": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 256 - tableBorderGray,
                                        "green": 256 - tableBorderGray,
                                        "blue": 256 - tableBorderGray
                                    }
                                },
                                "left": {
                                    "style": "SOLID",
                                    "color": {
                                        "red": 256 - tableBorderGray,
                                        "green": 256 - tableBorderGray,
                                        "blue": 256 - tableBorderGray
                                    }
                                },
                                "right": {
                                    "style": "SOLID", 
                                    "color": {
                                        "red": 256 - tableBorderGray,
                                        "green": 256 - tableBorderGray,
                                        "blue": 256 - tableBorderGray
                                    }
                                }
                            } 
                        }

        # Add Borders
        self.borders = {
                            "borders": {
                                "top": {
                                    "style": "SOLID"
                                },
                                "bottom": {
                                    "style": "SOLID"
                                },
                                "left": {
                                    "style": "SOLID"
                                },
                                "right": {
                                    "style": "SOLID"
                                }
                            } 
                        }
