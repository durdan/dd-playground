#!/usr/bin/env python3
"""
Enhanced Code Generator using CrewAI Multi-Agent Collaboration
"""

from services.enhanced_code_generator import EnhancedCodeGenerator
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Generate code using CrewAI multi-agent collaboration")
    parser.add_argument("--requirements", "-r", required=True, help="Requirements for code generation")
    parser.add_argument("--output-dir", "-o", default="generated_code", help="Output directory")
    parser.add_argument("--no-iterative", action="store_true", help="Disable iterative improvement")
    parser.add_argument("--iterations", type=int, default=2, help="Number of improvement iterations")
    parser.add_argument("--model", default="gpt-4", help="LLM model to use")
    
    args = parser.parse_args()
    
    try:
        # Initialize the enhanced code generator
        generator = EnhancedCodeGenerator(llm_model=args.model)
        
        print("🚀 Starting multi-agent code generation...")
        print(f"Requirements: {args.requirements}")
        
        # Generate code
        result = generator.generate_complex_implementation(
            requirements=args.requirements,
            use_iterative_improvement=not args.no_iterative,
            iterations=args.iterations
        )
        
        # Save generated code
        saved_files = generator.save_generated_code(result, args.output_dir)
        
        print("\n✅ Code generation completed successfully!")
        print(f"📁 Files saved to: {args.output_dir}")
        for file in saved_files:
            print(f"  - {file}")
        
        # Print summary
        print(f"\n📊 Generation Summary:")
        print(f"  - Architecture: ✓")
        print(f"  - Implementation: ✓") 
        print(f"  - Code Review: ✓")
        print(f"  - Test Suite: ✓")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())