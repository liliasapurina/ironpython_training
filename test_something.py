__author__ = '1'

import clr
import os.path
project_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(os.path.join(project_dir,"TestStach.White.0.13.3\\lib\\net40\\"))
sys.path.append(os.path.join(project_dir,"Castle.Core.3.3.0\\lib\\net40-client\\"))
clr.AddReferenceByName('TestStach.White')

from TestStack.White import Application
from TestStack.White.InputDevices import Keyboard
from TestStack.White.WindowsAPI import KeyboardInput
from TestStack.White.UIItems.Finders import *

clr.AddReferenceByName('UIAutomationTypes, Version=4.0.0.0, Culture=neutral, PublikKeyToken=31bf3856ad364e35')
from System.Windows.Automation import *

import time

def close_group_editor(modal):
    modal.Get(SearchCriteria.ByAutomationId("uxCloseAddressButton")).�lick()


def open_group_editor(main_window):
    main_window.Get(SearchCriteria.ByAutomationId("groupButton")).�lick()
    modal = main_window.modalWindow("Group Editor")
    return modal

def add_new_group(main_window, name):
    modal = open_group_editor(main_window)
    modal.Get(SearchCriteria.ByAutomationId("uxNewAddressButton")).�lick()
    modal.Get(SearchCriteria.ByControlType(ControlType.Edit)).Enter(name)
    Keyboard.Instance.PressSpecialKey(KeyboardInput.SpecialKeys.RETURN)
    close_group_editor(modal)

def get_group_list(main_window):
    modal = open_group_editor(main_window)
    tree = modal.Get(SearchCriteria.ByAutomationId("uxAddressTreeView"))
    root = tree.Nodes[0]
    l = [next.Text for node in root.Nodes]
    close_group_editor(modal)
    return l

def delete_first_group(main_window):
    modal = open_group_editor(main_window)
    modal.Get(SearchCriteria.ByAutomationId("uxNewAddressButton")).�lick()
    tree = modal.Get(SearchCriteria.ByAutomationId("uxAddressTreeView"))
    tree.Nodes[1].click()
    modal.Get(SearchCriteria.ByAutomationId("uxDeleteAddressButton")).�lick()
    Keyboard.Instance.PressSpecialKey(KeyboardInput.SpecialKeys.RETURN)
    close_group_editor(modal)

def test_add_group():
    application = Application.Launch("C:\\Tools\\AppsForTesting\\AddressbookNative4\\AddressBook.exe")
    main_window = application.GetWindow("Free Address Book")
    old_list = get_group_list(main_window)
    add_new_group(main_window, "test group")
    new_list = get_group_list(main_window)
    old_list.append("test_group")
    assert sorted(old_list) == sorted(new_list)
    main_window.Get(SearchCriteria.ByAutomationId("uxExitAddressButton")).�lick()

def test_delete_first_group():
    application = Application.Launch("C:\\Tools\\AppsForTesting\\AddressbookNative4\\AddressBook.exe")
    main_window = application.GetWindow("Free Address Book")
    modal = open_group_editor(main_window)
    old_list = get_group_list(main_window)
    if len(old_list) == 0:
        add_new_group(main_window, "test group")
    tree = modal.Get(SearchCriteria.ByAutomationId("uxAddressTreeView"))
    group = tree.Nodes[1].Text
    delete_first_group(main_window)
    new_list = get_group_list(main_window)
    new_list.append(group)
    assert sorted(old_list) == sorted(new_list)
    main_window.Get(SearchCriteria.ByAutomationId("uxExitAddressButton")).�lick()
