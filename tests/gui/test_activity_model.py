"""Tests for ActivityModel."""

from mygoog_gui.widgets.activity import ActivityModel, ActivityItem, ActivityStatus

def test_activity_model_initial_empty():
    """Test that model is initially empty."""
    model = ActivityModel()
    assert model.rowCount() == 0

def test_add_activity():
    """Test adding an activity."""
    model = ActivityModel()
    item = ActivityItem(id="1", title="Test Task")
    model.add_activity(item)
    
    assert model.rowCount() == 1
    assert model.data(model.index(0), ActivityModel.TitleRole) == "Test Task"
    assert model.data(model.index(0), ActivityModel.StatusRole) == ActivityStatus.PENDING

def test_update_status():
    """Test updating activity status."""
    model = ActivityModel()
    item = ActivityItem(id="sync_1", title="Sync Folder")
    model.add_activity(item)
    
    model.update_status("sync_1", ActivityStatus.RUNNING, "Scanning files...")
    
    assert model.data(model.index(0), ActivityModel.StatusRole) == ActivityStatus.RUNNING
    assert model.data(model.index(0), ActivityModel.DetailsRole) == "Scanning files..."

def test_update_nonexistent_activity():
    """Test updating status of an activity that doesn't exist (should not crash)."""
    model = ActivityModel()
    model.update_status("none", ActivityStatus.SUCCESS)
    assert model.rowCount() == 0


