"""
Tests for the review progress tracking functionality.
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from vaahai.review.steps.progress import ReviewProgress, ReviewStepStatus


class TestReviewProgress(unittest.TestCase):
    """Test cases for the ReviewProgress class."""

    def setUp(self):
        """Set up test fixtures."""
        self.progress = ReviewProgress()

    def test_register_step(self):
        """Test registering a review step."""
        self.progress.register_step("test_step")
        self.assertIn("test_step", self.progress.step_statuses)
        self.assertEqual(self.progress.step_statuses["test_step"], ReviewStepStatus.PENDING)
        self.assertIn("test_step", self.progress.step_times)
        self.assertEqual(self.progress.step_times["test_step"]["start_time"], 0.0)
        self.assertEqual(self.progress.step_times["test_step"]["end_time"], 0.0)
        self.assertEqual(self.progress.step_times["test_step"]["duration"], 0.0)

    def test_register_steps(self):
        """Test registering multiple review steps."""
        self.progress.register_steps(["step1", "step2", "step3"])
        self.assertIn("step1", self.progress.step_statuses)
        self.assertIn("step2", self.progress.step_statuses)
        self.assertIn("step3", self.progress.step_statuses)
        self.assertEqual(self.progress.step_statuses["step1"], ReviewStepStatus.PENDING)
        self.assertEqual(self.progress.step_statuses["step2"], ReviewStepStatus.PENDING)
        self.assertEqual(self.progress.step_statuses["step3"], ReviewStepStatus.PENDING)

    @patch("time.time")
    def test_start_step(self, mock_time):
        """Test starting a review step."""
        mock_time.return_value = 100.0
        self.progress.start_step("test_step")
        self.assertEqual(self.progress.step_statuses["test_step"], ReviewStepStatus.IN_PROGRESS)
        self.assertEqual(self.progress.step_times["test_step"]["start_time"], 100.0)
        self.assertEqual(self.progress.current_step, "test_step")

    @patch("time.time")
    def test_complete_step(self, mock_time):
        """Test completing a review step."""
        # Start the step
        mock_time.return_value = 100.0
        self.progress.start_step("test_step")
        
        # Complete the step
        mock_time.return_value = 105.0
        self.progress.complete_step("test_step")
        
        self.assertEqual(self.progress.step_statuses["test_step"], ReviewStepStatus.COMPLETED)
        self.assertEqual(self.progress.step_times["test_step"]["end_time"], 105.0)
        self.assertEqual(self.progress.step_times["test_step"]["duration"], 5.0)
        self.assertIsNone(self.progress.current_step)

    @patch("time.time")
    def test_fail_step(self, mock_time):
        """Test failing a review step."""
        # Start the step
        mock_time.return_value = 100.0
        self.progress.start_step("test_step")
        
        # Fail the step
        mock_time.return_value = 103.0
        self.progress.fail_step("test_step")
        
        self.assertEqual(self.progress.step_statuses["test_step"], ReviewStepStatus.FAILED)
        self.assertEqual(self.progress.step_times["test_step"]["end_time"], 103.0)
        self.assertEqual(self.progress.step_times["test_step"]["duration"], 3.0)
        self.assertIsNone(self.progress.current_step)

    def test_skip_step(self):
        """Test skipping a review step."""
        self.progress.skip_step("test_step")
        self.assertEqual(self.progress.step_statuses["test_step"], ReviewStepStatus.SKIPPED)

    def test_get_step_status(self):
        """Test getting the status of a review step."""
        self.progress.register_step("test_step")
        self.assertEqual(self.progress.get_step_status("test_step"), ReviewStepStatus.PENDING)
        
        self.progress.start_step("test_step")
        self.assertEqual(self.progress.get_step_status("test_step"), ReviewStepStatus.IN_PROGRESS)
        
        self.progress.complete_step("test_step")
        self.assertEqual(self.progress.get_step_status("test_step"), ReviewStepStatus.COMPLETED)

    def test_get_step_duration(self):
        """Test getting the duration of a review step."""
        # Register a step but don't start it
        self.progress.register_step("test_step")
        self.assertEqual(self.progress.get_step_duration("test_step"), 0.0)
        
        # Start and complete the step with a mocked duration
        with patch("time.time") as mock_time:
            mock_time.return_value = 100.0
            self.progress.start_step("test_step")
            
            mock_time.return_value = 105.0
            self.progress.complete_step("test_step")
        
        self.assertEqual(self.progress.get_step_duration("test_step"), 5.0)
        
        # Test with an unregistered step
        self.assertEqual(self.progress.get_step_duration("unknown_step"), 0.0)

    def test_get_progress_summary(self):
        """Test getting a summary of the review progress."""
        # Register and start multiple steps
        with patch("time.time") as mock_time:
            # Step 1: Completed
            mock_time.return_value = 100.0
            self.progress.start_step("step1")
            mock_time.return_value = 105.0
            self.progress.complete_step("step1")
            
            # Step 2: Failed
            mock_time.return_value = 110.0
            self.progress.start_step("step2")
            mock_time.return_value = 112.0
            self.progress.fail_step("step2")
            
            # Step 3: In progress
            mock_time.return_value = 115.0
            self.progress.start_step("step3")
            
            # Step 4: Pending
            self.progress.register_step("step4")
            
            # Step 5: Skipped
            self.progress.skip_step("step5")
        
        summary = self.progress.get_progress_summary()
        
        self.assertEqual(summary["total_steps"], 5)
        self.assertEqual(summary["completed_steps"], 1)
        self.assertEqual(summary["in_progress_steps"], 1)
        self.assertEqual(summary["failed_steps"], 1)
        self.assertEqual(summary["skipped_steps"], 1)
        self.assertEqual(summary["pending_steps"], 1)
        self.assertEqual(summary["progress_percentage"], 40.0)  # (1 completed + 1 skipped) / 5 * 100
        self.assertEqual(summary["total_duration"], 7.0)  # 5.0 (step1) + 2.0 (step2)
        self.assertEqual(summary["current_step"], "step3")

    def test_reset(self):
        """Test resetting the progress tracker."""
        # Register and start a step
        self.progress.register_step("test_step")
        self.progress.start_step("test_step")
        
        # Reset the progress tracker
        self.progress.reset()
        
        self.assertEqual(len(self.progress.step_statuses), 0)
        self.assertEqual(len(self.progress.step_times), 0)
        self.assertIsNone(self.progress.current_step)


if __name__ == "__main__":
    unittest.main()
