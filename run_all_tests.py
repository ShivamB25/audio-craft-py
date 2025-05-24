#!/usr/bin/env python3
"""
Comprehensive test runner for the Audio Generation Library.
Runs all test scripts and provides a summary of results.
"""

import subprocess
import sys
import os
from datetime import datetime
from typing import Tuple


class TestRunner:
    """Test runner for all audio generation library tests."""

    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None

    def run_command(self, command: str, description: str) -> Tuple[bool, str]:
        """Run a command and return success status and output."""
        print(f"\n{'='*60}")
        print(f"🧪 Running: {description}")
        print(f"Command: {command}")
        print("=" * 60)

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout per test
            )

            # Print output in real-time style
            if result.stdout:
                print("📤 STDOUT:")
                print(result.stdout)

            if result.stderr:
                print("📤 STDERR:")
                print(result.stderr)

            success = result.returncode == 0
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"\n{status} - {description}")

            return success, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT - {description} (exceeded 5 minutes)")
            return False, "Test timed out after 5 minutes"
        except Exception as e:
            print(f"💥 ERROR - {description}: {str(e)}")
            return False, f"Exception: {str(e)}"

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        print("🔍 Checking Prerequisites")
        print("=" * 40)

        # Check Python version
        python_version = sys.version_info
        print(
            f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}"
        )
        if python_version < (3, 12):
            print("❌ Python 3.12+ required")
            return False
        print("✅ Python version OK")

        # Check API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment")
            print("   Please set your API key in .env file or environment variables")
            return False
        print("✅ GEMINI_API_KEY found")

        # Check if test files exist
        test_files = [
            "tests/test_example.py",
            "tests/test_languages.py",
            "tests/test_voice_options.py",
            "tests/test_multi_speaker.py",
            "main.py",
        ]

        missing_files = []
        for file in test_files:
            if not os.path.exists(file):
                missing_files.append(file)

        if missing_files:
            print(f"❌ Missing test files: {', '.join(missing_files)}")
            return False
        print("✅ All test files found")

        # Check output directory
        if not os.path.exists("output"):
            print("📁 Creating output directory...")
            os.makedirs("output", exist_ok=True)
        print("✅ Output directory ready")

        return True

    def run_all_tests(self):
        """Run all test scripts."""
        self.start_time = datetime.now()

        print("🎵 Audio Generation Library - Comprehensive Test Suite")
        print("=" * 70)
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Check prerequisites first
        if not self.check_prerequisites():
            print("\n❌ Prerequisites not met. Aborting tests.")
            return False

        # Define all tests to run
        tests = [
            ("python tests/test_example.py", "Basic Functionality Test"),
            (
                "python tests/test_languages.py",
                "Multi-Language Support Test (24 languages)",
            ),
            ("python tests/test_voice_options.py", "Voice Options Test (30 voices)"),
            ("python tests/test_multi_speaker.py", "Multi-Speaker TTS Test"),
            ("python main.py", "Comprehensive Examples"),
        ]

        # Run each test
        for command, description in tests:
            success, output = self.run_command(command, description)
            self.test_results.append(
                {
                    "command": command,
                    "description": description,
                    "success": success,
                    "output": output,
                }
            )

        self.end_time = datetime.now()
        self.print_summary()

        return all(result["success"] for result in self.test_results)

    def print_summary(self):
        """Print test summary."""
        duration = self.end_time - self.start_time

        print(f"\n{'='*70}")
        print("📊 TEST SUMMARY")
        print("=" * 70)

        passed = sum(1 for result in self.test_results if result["success"])
        failed = len(self.test_results) - passed

        print(f"⏱️  Total Duration: {duration}")
        print(f"📈 Tests Run: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Success Rate: {(passed/len(self.test_results)*100):.1f}%")

        print("\n📋 Detailed Results:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"  {i}. {status} - {result['description']}")

        if failed > 0:
            print("\n🔍 Failed Test Details:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"\n❌ {result['description']}")
                    print(f"   Command: {result['command']}")
                    # Show last few lines of output for failed tests
                    output_lines = result["output"].split("\n")[-10:]
                    for line in output_lines:
                        if line.strip():
                            print(f"   {line}")

        print("\n📁 Generated Files:")
        if os.path.exists("output"):
            output_files = os.listdir("output")
            if output_files:
                for file in sorted(output_files):
                    file_path = os.path.join("output", file)
                    file_size = os.path.getsize(file_path)
                    print(f"   📄 {file} ({file_size:,} bytes)")
            else:
                print("   (No files generated)")

        # Overall result
        if failed == 0:
            print(
                "\n🎉 ALL TESTS PASSED! The Audio Generation Library is working perfectly."
            )
            print(
                "   🎧 You can listen to the generated audio files in the output/ directory"
            )
            print("   📚 Check the docs/ directory for comprehensive usage examples")
        else:
            print(
                f"\n⚠️  {failed} test(s) failed. Please check the error details above."
            )
            print(
                "   💡 Common issues: API key problems, network connectivity, missing dependencies"
            )

        print("=" * 70)


def main():
    """Main function to run all tests."""
    runner = TestRunner()

    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
