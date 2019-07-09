import pygame;

# Controller as in this class controls the gamepads
class Input_Controller:
    def __init__(self):
        self.gamepad_types = [];
        self.gamepad_list = self.gamepad_setup();


    #############################################################
    #######################Keyboard input handling
    def keyboard_and_mouse_input_controller(self, event, player_one, player_two):
        # Keyboard input
        if(event.type == pygame.KEYDOWN):
            self.press_key(event.key, player_one, player_two);
        elif(event.type == pygame.KEYUP):
            self.release_key(event.key, player_one, player_two);

        # Mouse input
        if(event.type == pygame.MOUSEMOTION):
            self.move_mouse(player_one); # Only player one may use a mouse at this time


    def press_key(self, event_key, player_one, player_two):
        # Player one input
        if(event_key == pygame.K_w):
            player_one.move_controller_y(-1);
        elif(event_key == pygame.K_s):
            player_one.move_controller_y(1);

        if(event_key == pygame.K_d):
            player_one.move_controller_x(1);
        elif(event_key == pygame.K_a):
            player_one.move_controller_x(-1);

        if(event_key == pygame.K_k):
            player_one.player_attack();

        # Player two input
        if(event_key == pygame.K_UP):
            player_two.move_controller_y(-1);
        elif(event_key == pygame.K_DOWN):
            player_two.move_controller_y(1);
        if(event_key == pygame.K_RIGHT):
            player_two.move_controller_x(1);
        elif(event_key == pygame.K_LEFT):
            player_two.move_controller_x(-1);

        # if(event_key == pygame.K_p):
        #    box.move(self.player_one.location)


    def release_key(self, event_key, player_one, player_two):
        if(event_key == pygame.K_w):
            player_one.move_controller_y(0);
        if(event_key == pygame.K_s):
            player_one.move_controller_y(0);
        if(event_key == pygame.K_d):
            player_one.move_controller_x(0);
        if(event_key == pygame.K_a):
            player_one.move_controller_x(0);

        if(event_key == pygame.K_UP):
            player_two.move_controller_y(0);
        if(event_key == pygame.K_DOWN):
            player_two.move_controller_y(0);
        if(event_key == pygame.K_RIGHT):
            player_two.move_controller_x(0);
        if(event_key == pygame.K_LEFT):
            player_two.move_controller_x(0);


    def move_mouse(self, player_one):
        player_one.mouse_move_aiming_reticule(pygame.mouse.get_pos());


    ###############################################################
    ########################Gamepad input handling
    def gamepad_input_controller(self, event, player_one, player_two):
        if(event.type == pygame.JOYBUTTONDOWN):
            self.gamepad_button_input_handler(event, player_one, player_two);

        elif(event.type == pygame.JOYAXISMOTION):
            # Check if the axis is on the D-pad on an older controller
            if(self.gamepad_list[event.joy].get_numhats() == 0):
                self.gamepad_dpad_input_handler(event, player_one, player_two);
            else: # Analog stick on modern controllers
                self.gamepad_analog_stick_input_handler(event, player_one, player_two);

        # D-pad input on modern controllers
        elif(event.type == pygame.JOYHATMOTION):
            self.gamepad_hat_input_handler(event, player_one, player_two);


    def gamepad_button_input_handler(self, event, player_one, player_two):
        # Print which button was pressed
        print(self.gamepad_types[event.joy].get_type_button(event.button));

        # Player one input controls
        if (self.gamepad_list[event.joy].get_id() == 0):
            if (event.button == 0): # B button
                player_one.player_attack();
            elif (event.button == 1): # A Button
                #box.move(self.player_one.location);
                u = 0;

            elif (event.button == 9):
                # Start button
                u = 0;
            elif (event.button == 8):
                # Select button
                u = 0;

        # Player two input controls
        elif (self.gamepad_list[event.joy].get_id() == 1):
            if (event.button == 0): # B button
                player_two.player_attack();
            elif (event.button == 1): # A button
                #box.move(self.player_two.location);
                u = 0;

            elif(event.button == 9):
                # Start button
                u = 0;
            elif(event.button == 8):
                # Select button
                u = 0;


    def gamepad_dpad_input_handler(self, event, player_one, player_two):
        # D-pad movement
        axis = self.gamepad_list[event.joy].get_axis(event.axis);

        # Player 1 D-pad controls
        if (self.gamepad_list[event.joy].get_id() == 0):
            if (event.axis == 1):
                if (axis == 0.999969482421875):
                    player_one.move_controller_y(1);
                elif (axis == -1.0):
                    player_one.move_controller_y(-1);
                else:
                    player_one.move_controller_y(0);
            else:
                if (axis == 0.999969482421875):
                    player_one.move_controller_x(1);
                elif (axis == -1.0):
                    player_one.move_controller_x(-1);
                else:
                    player_one.move_controller_x(0);

        # Player 2 D-pad controls
        elif (self.gamepad_list[event.joy].get_id() == 1):
            if (event.axis == 1):
                if (axis == 0.999969482421875):
                    player_two.move_controller_y(1);
                elif (axis == -1.0):
                    player_two.move_controller_y(-1);
                else:
                    player_two.move_controller_y(0);
            else:
                if (axis == 0.999969482421875):
                    player_two.move_controller_x(1);
                elif (axis == -1.0):
                    player_two.move_controller_x(-1);
                else:
                    player_two.move_controller_x(0);


    def gamepad_analog_stick_input_handler(self, event, player_one, player_two):
        axis = self.gamepad_list[event.joy].get_axis(event.axis);

        # Player 1 analog stick controls
        if (self.gamepad_list[event.joy].get_id() == 0):
            # Left analog stick
            if(event.axis == 0):
                if(-1.0 <= axis <= -0.5):
                    player_one.move_controller_x(-1);
                elif(0.5 <= axis <= 1.0):
                    player_one.move_controller_x(1);
                else:
                    player_one.move_controller_x(0);

            elif(event.axis == 1):
                if(-1.0 <= axis <= -0.7):
                    player_one.move_controller_y(-1);
                elif(0.4 <= axis <= 1.0):
                    player_one.move_controller_y(1);
                else:
                    player_one.move_controller_y(0);

            # Right analog stick
            elif(event.axis == 2):
                if(axis == -1.0):
                    player_one.gamepad_move_aiming_reticule_x(-1);
                    print('R-LEFT');
                elif(axis > 0.9):
                    player_one.gamepad_move_aiming_reticule_x(1);
                    print('R-RIGHT');
                else:
                    player_one.gamepad_move_aiming_reticule_x(0);

            elif(event.axis == 3):
                if(-1.0 <= axis <= -0.5):
                    player_one.gamepad_move_aiming_reticule_y(-1);
                    print('R-UP');
                elif(axis > 0.9):
                    player_one.gamepad_move_aiming_reticule_y(1);
                    print('R-DOWN');
                else:
                    player_one.gamepad_move_aiming_reticule_y(0);
                print(axis);

        # Player 2 analog controls
        elif(self.gamepad_list[event.joy].get_id() == 1):
            # Left analog stick
            if(event.axis == 0):
                if (-1.0 <= axis <= -0.5):
                    player_two.move_controller_x(-1);
                elif (0.5 <= axis <= 1.0):
                    player_two.move_controller_x(1);
                else:
                    player_two.move_controller_x(0);

            elif (event.axis == 1):
                if (-1.0 <= axis <= -0.7):
                    player_two.move_controller_y(-1);
                elif (0.4 <= axis <= 1.0):
                    player_two.move_controller_y(1);
                else:
                    player_two.move_controller_y(0);

            # Right analog stick
            elif(event.axis == 2):
                if(axis == -1.0):
                    print('R-LEFT');
                elif(axis > 0.9):
                    print('R-RIGHT');
            elif(event.axis == 3):
                if(axis == -1.0):
                    print('R-UP');
                elif(axis > 0.9):
                    print('R-DOWN');


    def gamepad_hat_input_handler(self, event, player_one, player_two):
        axis = self.gamepad_list[event.joy].get_hat(0);

        if (self.gamepad_list[event.joy].get_id() == 0):
            player_one.move_controller_y(-axis[1]);
            player_one.move_controller_x(axis[0]);
        elif (self.gamepad_list[event.joy].get_id() == 1):
            player_two.move_controller_y(-axis[1]);
            player_two.move_controller_x(axis[0]);
    #################################################################


    def gamepad_setup(self):
        gamepad_list = [];
        for gamepad in range(0, pygame.joystick.get_count()):
            gamepad_list.append(pygame.joystick.Joystick(gamepad));

        for gamepad in gamepad_list:
            gamepad.init();

            if(gamepad.get_init()):
                self.gamepad_types.append(
                    Gamepad_Type(
                        gamepad.get_name(),
                        gamepad.get_numbuttons()
                    )
                );

                gamepad_name = self.gamepad_types[gamepad.get_id()].get_gamepad_type();
                self.print_gamepad_info(gamepad, gamepad_name);

            else:
                print('Gamepad initialization failed!');

        return gamepad_list;


    def print_gamepad_info(self, gamepad, gamepad_name):
        print(gamepad.get_name());
        print('------------------------------------------------');
        print('Detected input: ' + gamepad_name + ' controller');
        print('------------------------------------------------');
        print('Gamepad ID: ' + str(gamepad.get_id()));
        print('Num of buttons: ' + str(gamepad.get_numbuttons()));
        print('Num of D-pads: ' + str(gamepad.get_numhats()));
        print('Axes: ' + str(gamepad.get_numaxes()));
        print('------------------------------------------------');
        print();


    def disable_gamepads(self):
        pygame.joystick.quit();


    def get_gamepad_list(self):
        return self.gamepad_list;


    def get_gamepad_count(self):
        return len(self.gamepad_list);


# Used to keep track of the type of gamepad being used (Xbox, Playstation etc.).
# Also has Switch Joycon support just for fun.
class Gamepad_Type:
    def __init__(self, gamepad, num_of_buttons):
        self.type = self.detect_gamepad_type(gamepad, num_of_buttons);
        self.button_list = self.initialize_button_list();


    def detect_gamepad_type(self, gamepad, num_of_buttons):
        if('XBOX' in gamepad or 'xbox' in gamepad or 'Xbox' in gamepad):
            return 'XBOX';

        elif('PS' in gamepad or 'Playstation' in gamepad or 'playstation' in gamepad
             or 'PLAYSTATION' in gamepad or 'dualshock' in gamepad or 'Dualshock' in gamepad
             or 'DUALSHOCK' in gamepad):
                return 'DUALSHOCK';

        elif('Wireless' in gamepad):
            if(num_of_buttons == 14):
                return 'DUALSHOCK';
            if(num_of_buttons == 16):
                return 'JOYCON';


    def initialize_button_list(self):
        if(self.type == 'XBOX'):
            return [
                'X', 'A', 'B', 'Y',
                'LB', 'RB', 'LT', 'RT',
                'Back', 'Start',
                'Left stick', 'Right stick',
                'Guide'
            ];
        elif(self.type == 'DUALSHOCK'):
            return [
                '◻', '✖', 'O', '△', # Symbols won't be used later
                'L1', 'R1', 'L2', 'R2',
                'Share', 'Options',
                'L3', 'R3',
                'Home', 'Touchpad'
            ];

        elif(self.type == 'JOYCON'):
            return [
                'A', 'X', 'B', 'Y',
                'SL', 'SR',
                '', '', '',
                '+/-',
                '',
                'Analog stick',
                'Home',
                '',
                'R', 'ZR',
            ];


    def get_gamepad_type(self):
        return self.type;


    def get_type_button(self, button_id):
        return self.button_list[button_id];