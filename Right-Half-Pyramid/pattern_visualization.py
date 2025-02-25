from manim import *

class CodeExecutionVisualization(Scene):
    def construct(self):
        # The original code to visualize
        code_str = """n = int(input())
for i in range(1, n+1):
    for j in range(1, i+1):
        print('*', end="")
    print()"""
        
        # Create the code block with better syntax highlighting
        code = Code(
            code=code_str,
            tab_width=4,
            background="window",
            language="python",
            font="Monospace",
            font_size=24,
            line_spacing=0.7,  # Better spacing between lines
        )
        code.to_edge(LEFT, buff=1)
        
        # Store the original code string for later use
        self.code_lines = code_str.split("\n")
        
        # Create output display area - make it larger to prevent overflow
        output_box = RoundedRectangle(
            height=5,  # Increased height
            width=6,   # Increased width
            corner_radius=0.1,
            stroke_color=WHITE,
        )
        output_box.to_edge(RIGHT, buff=1)
        output_title = Text("Output", font_size=24).next_to(output_box, UP)
        output_group = VGroup(output_box, output_title)
        
        # Create a container for output text - initialize with space to avoid empty text alignment issues
        output_text = Text(" ", font="Monospace", font_size=28)
        # Position the output text inside the box with better anchoring
        output_text.move_to(output_box.get_center())
        # Get the corner position directly instead of using align_to on empty text
        initial_pos = output_box.get_corner(UL) + DOWN * 0.4 + RIGHT * 0.4
        output_text.move_to(initial_pos)
        
        # Create variable tracker display
        var_tracker_box = RoundedRectangle(
            height=1.5,
            width=4,
            corner_radius=0.1,
            stroke_color=BLUE_D,
            fill_color=BLACK,
            fill_opacity=0.8
        )
        var_tracker_box.next_to(code, DOWN, buff=0.5)
        var_tracker_title = Text("Variables", font_size=20).next_to(var_tracker_box, UP, buff=0.1)
        var_tracker_text = Text("n = 5", font="Monospace", font_size=20)
        var_tracker_text.move_to(var_tracker_box.get_center())
        var_tracker_group = VGroup(var_tracker_box, var_tracker_title, var_tracker_text)
        
        # Show title
        title = Text("Pattern Printing Algorithm Visualization", font_size=32)
        title.to_edge(UP)
        
        # Setup initial scene
        self.play(Write(title))
        self.play(Create(code), Create(output_group), Create(var_tracker_group))
        self.wait(1)
        
        # Define n value for the example
        n_value = 5
        
        # Create a cursor to highlight current line with better appearance
        cursor = Rectangle(
            width=code.width,
            height=code.height / len(self.code_lines) * 0.9,  # Slightly smaller for better appearance
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2,
            stroke_color=YELLOW,
            stroke_opacity=0.8
        )
        cursor.align_to(code, UL).shift(DOWN * 0.1)  # Adjust position
        
        # Add everything to scene
        self.add(cursor, output_text)
        
        # Execute and visualize the code
        # Line 1: n = int(input())
        self.highlight_line(cursor, code, 0)
        n_text = Text(f"n = {n_value}", font="Monospace", font_size=24)
        n_text.next_to(code, UP).to_edge(LEFT, buff=1)
        self.play(Write(n_text))
        self.wait(1)
        
        # Output display
        current_output = ""
        
        # Line 2: for i in range(1, n+1):
        self.highlight_line(cursor, code, 1)
        self.update_variables(var_tracker_text, f"n = {n_value}")
        self.wait(1)
        
        # Simulate the outer loop
        for i in range(1, n_value+1):
            # Update variables display with i
            self.update_variables(var_tracker_text, f"n = {n_value}\ni = {i}")
            
            # Line 3: for j in range(1, i+1):
            self.highlight_line(cursor, code, 2)
            self.wait(0.5)
            
            # Create a new line for this iteration
            current_line = ""
            
            # Simulate the inner loop
            for j in range(1, i+1):
                # Update variables display with j
                self.update_variables(var_tracker_text, f"n = {n_value}\ni = {i}\nj = {j}")
                
                # Line 4: print('*', end="")
                self.highlight_line(cursor, code, 3)
                
                # Update the current line with a star
                current_line += "*"
                
                # Temporarily display partial line
                if current_output:
                    temp_output = current_output + "\n" + current_line
                else:
                    temp_output = current_line
                    
                # Update output display with incremental changes
                new_output_text = Text(temp_output, font="Monospace", font_size=28)
                # Position the new output text consistently with better alignment
                new_output_text.move_to(output_box.get_center())
                initial_pos = output_box.get_corner(UL) + DOWN * 0.4 + RIGHT * 0.4
                new_output_text.move_to(initial_pos, aligned_edge=UL)
                self.play(Transform(output_text, new_output_text), run_time=0.2)
                self.wait(0.2)
            
            # Line 5: print()
            self.highlight_line(cursor, code, 4)
            
            # Add the completed line to the output
            if current_output:
                current_output += "\n" + current_line
            else:
                current_output = current_line
                
            # Update output display
            new_output_text = Text(current_output, font="Monospace", font_size=28)
            # Position the new output text consistently
            new_output_text.move_to(output_box.get_center())
            initial_pos = output_box.get_corner(UL) + DOWN * 0.4 + RIGHT * 0.4
            new_output_text.move_to(initial_pos, aligned_edge=UL)
            self.play(Transform(output_text, new_output_text), run_time=0.2)
            
            # Back to the outer loop
            self.highlight_line(cursor, code, 1)
            self.wait(0.5)
        
        # Conclusion
        self.wait(1)
        conclusion = Text("Execution Complete", color=GREEN, font_size=32)
        conclusion.next_to(title, DOWN)
        self.play(Write(conclusion))
        self.wait(2)
    
    def highlight_line(self, cursor, code, line_number):
        """Move the cursor to highlight a specific line of code."""
        line_height = code.height / len(self.code_lines)
        
        # Calculate position for cursor
        target_y = code.get_top()[1] - line_height * line_number - line_height/2
        target_position = cursor.copy()
        target_position.move_to([code.get_center()[0], target_y, 0])
        
        self.play(Transform(cursor, target_position), run_time=0.3)
    
    def update_variables(self, var_text, new_content):
        """Update the variable tracker display."""
        new_var_text = Text(new_content, font="Monospace", font_size=20)
        new_var_text.move_to(var_text.get_center())
        self.play(Transform(var_text, new_var_text), run_time=0.2)


if __name__ == "__main__":
    # Run with: python -m manim -pql <filename>.py CodeExecutionVisualization
    scene = CodeExecutionVisualization()
    scene.render()