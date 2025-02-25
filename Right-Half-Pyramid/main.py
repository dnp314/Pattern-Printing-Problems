from manim import *
import sys
from io import StringIO

class CodeExecutionVisualization(Scene):
    def construct(self):
        # The original code to visualize
        code_str = """n = int(input())
for i in range(1, n+1):
    for j in range(1, i+1):
        print('*', end="")
    print()"""
        
        # Create the code block
        code = Code(
            code=code_str,
            tab_width=4,
            background="window",
            language="python",
            font="Monospace",
            font_size=24,
        )
        code.to_edge(LEFT, buff=1)
        
        # Create output display area
        output_box = RoundedRectangle(
            height=4,
            width=5,
            corner_radius=0.1,
            stroke_color=WHITE,
        )
        output_box.to_edge(RIGHT, buff=1)
        output_title = Text("Output", font_size=24).next_to(output_box, UP)
        output_group = VGroup(output_box, output_title)
        
        # Create a container for output text
        output_text = Text("", font="Monospace", font_size=28)
        output_text.align_to(output_box, UP+LEFT).shift(DOWN * 0.3 + RIGHT * 0.3)
        
        # Show title
        title = Text("Pattern Printing Algorithm Visualization", font_size=32)
        title.to_edge(UP)
        
        # Setup initial scene
        self.play(Write(title))
        self.play(Create(code), Create(output_group))
        self.wait(1)
        
        # Define n value for the example
        n_value = 5
        
        # Create a cursor to highlight current line
        cursor = Rectangle(
            width=code.width,
            height=code.height / len(code_str.split("\n")),
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_width=0,
        )
        cursor.align_to(code, UP+LEFT)
        
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
        self.wait(1)
        
        # Simulate the outer loop
        for i in range(1, n_value+1):
            # Line 3: for j in range(1, i+1):
            self.highlight_line(cursor, code, 2)
            self.wait(0.5)
            
            # Create a new line for this iteration
            current_line = ""
            
            # Simulate the inner loop
            for j in range(1, i+1):
                # Line 4: print('*', end="")
                self.highlight_line(cursor, code, 3)
                
                # Update the current line with a star
                current_line += "*"
                
                # Temporarily display partial line
                if current_output:
                    temp_output = current_output + "\n" + current_line
                else:
                    temp_output = current_line
                    
                # Update output display
                new_output_text = Text(temp_output, font="Monospace", font_size=28)
                new_output_text.align_to(output_box, UP+LEFT).shift(DOWN * 0.3 + RIGHT * 0.3)
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
            new_output_text.align_to(output_box, UP+LEFT).shift(DOWN * 0.3 + RIGHT * 0.3)
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
        code_lines = code.code.split("\n")
        line_height = code.height / len(code_lines)
        
        target_y = code.get_top()[1] - line_height * (line_number + 0.5)
        target_position = cursor.copy()
        target_position.move_to([code.get_center()[0], target_y, 0])
        
        self.play(Transform(cursor, target_position), run_time=0.3)


if __name__ == "__main__":
    # Run with: python -m manim -pql <filename>.py CodeExecutionVisualization
    scene = CodeExecutionVisualization()
    scene.render()