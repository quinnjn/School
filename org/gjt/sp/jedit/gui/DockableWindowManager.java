/*
 * DockableWindowManager.java - manages dockable windows
 * :tabSize=8:indentSize=8:noTabs=false:
 * :folding=explicit:collapseFolds=1:
 *
 * Copyright (C) 2000, 2001 Slava Pestov
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

package org.gjt.sp.jedit.gui;

//{{{ Imports
import bsh.EvalError;
import com.microstar.xml.*;
import org.gjt.sp.jedit.browser.VFSBrowser;
import org.gjt.sp.jedit.search.HyperSearchResults;
import org.gjt.sp.jedit.*;
import org.gjt.sp.util.Log;
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.io.*;
import java.util.*;
//}}}

/**
 * Manages dockable windows.
 * @author Slava Pestov
 * @version $Id$
 * @since jEdit 2.6pre3
 */
public class DockableWindowManager extends JPanel
{
	//{{{ Static part of class

	//{{{ Constants
	/**
	 * Floating position.
	 * @since jEdit 2.6pre3
	 */
	public static final String FLOATING = "floating";

	/**
	 * Top position.
	 * @since jEdit 2.6pre3
	 */
	public static final String TOP = "top";

	/**
	 * Left position.
	 * @since jEdit 2.6pre3
	 */
	public static final String LEFT = "left";

	/**
	 * Bottom position.
	 * @since jEdit 2.6pre3
	 */
	public static final String BOTTOM = "bottom";

	/**
	 * Right position.
	 * @since jEdit 2.6pre3
	 */
	public static final String RIGHT = "right";
	//}}}

	//{{{ loadDockableWindows() method
	/**
	 * Plugins shouldn't need to call this method.
	 * @since jEdit 4.0pre1
	 */
	public static boolean loadDockableWindows(String path, Reader in, ActionSet actionSet)
	{
		try
		{
			//Log.log(Log.DEBUG,jEdit.class,"Loading dockables from " + path);

			DockableListHandler dh = new DockableListHandler(path,actionSet);
			XmlParser parser = new XmlParser();
			parser.setHandler(dh);
			parser.parse(null, null, in);
			return true;
		}
		catch(XmlException xe)
		{
			int line = xe.getLine();
			String message = xe.getMessage();
			Log.log(Log.ERROR,jEdit.class,path + ":" + line
				+ ": " + message);
		}
		catch(Exception e)
		{
			Log.log(Log.ERROR,jEdit.class,e);
		}

		return false;
	} //}}}

	//{{{ registerDockableWindow() method
	public static void registerDockableWindow(String name, String code,
		boolean actions, ActionSet actionSet)
	{
		dockableWindowFactories.addElement(new Factory(name,code,
			actions,actionSet));
	} //}}}

	//{{{ getRegisteredDockableWindows() method
	public static String[] getRegisteredDockableWindows()
	{
		String[] retVal = new String[dockableWindowFactories.size()];
		for(int i = 0; i < dockableWindowFactories.size(); i++)
		{
			retVal[i] = ((Factory)dockableWindowFactories.elementAt(i)).name;
		}
		return retVal;
	} //}}}

	//{{{ DockableListHandler class
	static class DockableListHandler extends HandlerBase
	{
		//{{{ DockableListHandler constructor
		DockableListHandler(String path, ActionSet actionSet)
		{
			this.path = path;
			this.actionSet = actionSet;
			stateStack = new Stack();
			actions = true;
		} //}}}

		//{{{ resolveEntity() method
		public Object resolveEntity(String publicId, String systemId)
		{
			if("dockables.dtd".equals(systemId))
			{
				// this will result in a slight speed up, since we
				// don't need to read the DTD anyway, as AElfred is
				// non-validating
				return new StringReader("<!-- -->");

				/* try
				{
					return new BufferedReader(new InputStreamReader(
						getClass().getResourceAsStream
						("/org/gjt/sp/jedit/dockables.dtd")));
				}
				catch(Exception e)
				{
					Log.log(Log.ERROR,this,"Error while opening"
						+ " dockables.dtd:");
					Log.log(Log.ERROR,this,e);
				} */
			}

			return null;
		} //}}}

		//{{{ attribute() method
		public void attribute(String aname, String value, boolean isSpecified)
		{
			aname = (aname == null) ? null : aname.intern();
			value = (value == null) ? null : value.intern();

			if(aname == "NAME")
				dockableName = value;
			else if(aname == "NO_ACTIONS")
				actions = (value == "FALSE");
		} //}}}

		//{{{ doctypeDecl() method
		public void doctypeDecl(String name, String publicId,
			String systemId) throws Exception
		{
			if("DOCKABLES".equals(name))
				return;

			Log.log(Log.ERROR,this,path + ": DOCTYPE must be DOCKABLES");
		} //}}}

		//{{{ charData() method
		public void charData(char[] c, int off, int len)
		{
			String tag = peekElement();
			String text = new String(c, off, len);

			if (tag == "DOCKABLE")
			{
				code = text;
			}
		} //}}}

		//{{{ startElement() method
		public void startElement(String tag)
		{
			tag = pushElement(tag);
		} //}}}

		//{{{ endElement() method
		public void endElement(String name)
		{
			if(name == null)
				return;

			String tag = peekElement();

			if(name.equals(tag))
			{
				if(tag == "DOCKABLE")
				{
					registerDockableWindow(dockableName,
						code,actions,actionSet);
					// make default be true for the next
					// action
					actions = true;
				}

				popElement();
			}
			else
			{
				// can't happen
				throw new InternalError();
			}
		} //}}}

		//{{{ startDocument() method
		public void startDocument()
		{
			try
			{
				pushElement(null);
			}
			catch (Exception e)
			{
				e.printStackTrace();
			}
		} //}}}

		//{{{ Private members

		//{{{ Instance variables
		private String path;
		private ActionSet actionSet;

		private String dockableName;
		private String code;
		private boolean actions;

		private Stack stateStack;
		//}}}

		//{{{ pushElement() method
		private String pushElement(String name)
		{
			name = (name == null) ? null : name.intern();

			stateStack.push(name);

			return name;
		} //}}}

		//{{{ peekElement() method
		private String peekElement()
		{
			return (String) stateStack.peek();
		} //}}}

		//{{{ popElement() method
		private String popElement()
		{
			return (String) stateStack.pop();
		} //}}}

		//}}}
	} //}}}

	//{{{ Factory class
	static class Factory
	{
		String name;
		String code;

		//{{{ Factory constructor
		Factory(String name, String code, boolean actions, ActionSet actionSet)
		{
			this.name = name;
			this.code = code;
			if(actions)
			{
				actionSet.addAction(new OpenAction());
				actionSet.addAction(new ToggleAction());
				actionSet.addAction(new FloatAction());
			}
		} //}}}

		//{{{ createDockableWindow() method
		JComponent createDockableWindow(View view, String position)
		{
			try
			{
				BeanShell.getNameSpace().setVariable(
					"position",position);
			}
			catch(EvalError e)
			{
				Log.log(Log.ERROR,this,e);
			}
			JComponent win = (JComponent)BeanShell.eval(view,
				BeanShell.getNameSpace(),code);
			return win;
		} //}}}

		//{{{ OpenAction class
		class OpenAction extends EditAction
		{
			//{{{ OpenAction constructor
			OpenAction()
			{
				super(name);
			} //}}}

			//{{{ invoke() method
			public void invoke(View view)
			{
				view.getDockableWindowManager()
					.showDockableWindow(name);
			} //}}}

			//{{{ getCode() method
			public String getCode()
			{
				return "view.getDockableWindowManager()"
					+ ".showDockableWindow(\"" + name + "\");";
			} //}}}
		} //}}}

		//{{{ ToggleAction class
		class ToggleAction extends EditAction
		{
			//{{{ ToggleAction constructor
			ToggleAction()
			{
				super(name + "-toggle");
			} //}}}

			//{{{ invoke() method
			public void invoke(View view)
			{
				view.getDockableWindowManager()
					.toggleDockableWindow(name);
			} //}}}

			//{{{ isToggle() method
			public boolean isToggle()
			{
				return true;
			} //}}}

			//{{{ isSelected() method
			public boolean isSelected(View view)
			{
				return view.getDockableWindowManager()
					.isDockableWindowVisible(name);
			} //}}}

			//{{{ getCode() method
			public String getCode()
			{
				return "view.getDockableWindowManager()"
					+ ".toggleDockableWindow(\"" + name + "\");";
			} //}}}

			//{{{ getLabel() method
			public String getLabel()
			{
				String[] args = { jEdit.getProperty(name + ".label") };
				return jEdit.getProperty("view.docking.toggle.label",args);
			} //}}}
		} //}}}

		//{{{ FloatAction class
		class FloatAction extends EditAction
		{
			//{{{ FloatAction constructor
			FloatAction()
			{
				super(name + "-float");
			} //}}}

			//{{{ invoke() method
			public void invoke(View view)
			{
				view.getDockableWindowManager()
					.floatDockableWindow(name);
			} //}}}

			//{{{ getCode() method
			public String getCode()
			{
				return "view.getDockableWindowManager()"
					+ ".floatDockableWindow(\"" + name + "\");";
			} //}}}

			//{{{ getLabel() method
			public String getLabel()
			{
				String[] args = { jEdit.getProperty(name + ".label") };
				return jEdit.getProperty("view.docking.float.label",args);
			} //}}}
		} //}}}
	} //}}}

	private static Vector dockableWindowFactories;

	//{{{ Static initializer
	static
	{
		dockableWindowFactories = new Vector();
	} //}}}

	//}}}

	//{{{ Instance part of class

	//{{{ DockableWindowManager constructor
	/**
	 * Creates a new dockable window manager.
	 * @param view The view
	 * @since jEdit 2.6pre3
	 */
	public DockableWindowManager(View view)
	{
		setLayout(new DockableLayout());
		this.view = view;
		windows = new Hashtable();

		top = new PanelWindowContainer(this,TOP);
		left = new PanelWindowContainer(this,LEFT);
		bottom = new PanelWindowContainer(this,BOTTOM);
		right = new PanelWindowContainer(this,RIGHT);

		add(DockableLayout.TOP_BUTTONS,top.getButtonBox());
		add(DockableLayout.LEFT_BUTTONS,left.getButtonBox());
		add(DockableLayout.BOTTOM_BUTTONS,bottom.getButtonBox());
		add(DockableLayout.RIGHT_BUTTONS,right.getButtonBox());

		add(TOP,top.getDockablePanel());
		add(LEFT,left.getDockablePanel());
		add(BOTTOM,bottom.getDockablePanel());
		add(RIGHT,right.getDockablePanel());
	} //}}}

	//{{{ init() method
	/**
	 * Initialises dockable window manager.
	 * @since jEdit 2.6pre3
	 */
	public void init()
	{
		for(int i = 0; i < dockableWindowFactories.size(); i++)
		{
			Factory factory = (Factory)
				dockableWindowFactories.elementAt(i);
			Entry e;
			if(view.isPlainView())
				e = new Entry(factory,FLOATING);
			else
				e = new Entry(factory);
			windows.put(factory.name,e);
		}

		if(!view.isPlainView())
		{
			String lastTop = jEdit.getProperty("view.dock.top.last");
			if(lastTop != null)
				showDockableWindow(lastTop);

			String lastLeft = jEdit.getProperty("view.dock.left.last");
			if(lastLeft != null)
				showDockableWindow(lastLeft);

			String lastBottom = jEdit.getProperty("view.dock.bottom.last");
			if(lastBottom != null)
				showDockableWindow(lastBottom);

			String lastRight = jEdit.getProperty("view.dock.right.last");
			if(lastRight != null)
				showDockableWindow(lastRight);
		}
	} //}}}

	//{{{ getView() method
	/**
	 * Returns this dockable window manager's view.
	 * @since jEdit 4.0pre2
	 */
	public View getView()
	{
		return view;
	} //}}}

	//{{{ floatDockableWindow() method
	/**
	 * Opens a new instance of the specified dockable window in a floating
	 * container.
	 * @param name The dockable window name
	 * @return The new dockable window instance
	 * @since jEdit 4.1pre2
	 */
	public JComponent floatDockableWindow(String name)
	{
		Entry entry = (Entry)windows.get(name);
		if(entry == null)
		{
			Log.log(Log.ERROR,this,"Unknown dockable window: " + name);
			return null;
		}

		// create a copy of this dockable window and float it
		Entry newEntry = new Entry(entry.factory,FLOATING);
		newEntry.open();
		if(newEntry.win != null)
			newEntry.container.show(newEntry);
		return newEntry.win;
	} //}}}

	//{{{ showDockableWindow() method
	/**
	 * Opens the specified dockable window.
	 * @param name The dockable window name
	 * @since jEdit 2.6pre3
	 */
	public void showDockableWindow(String name)
	{
		Entry entry = (Entry)windows.get(name);
		if(entry == null)
		{
			Log.log(Log.ERROR,this,"Unknown dockable window: " + name);
			return;
		}

		if(entry.win == null)
			entry.open();

		if(entry.win != null)
			entry.container.show(entry);
		else
			/* an error occurred */;
	} //}}}

	//{{{ addDockableWindow() method
	/**
	 * Opens the specified dockable window. As of version 4.0pre1, has the same
	 * effect as calling showDockableWindow().
	 * @param name The dockable window name
	 * @since jEdit 2.6pre3
	 */
	public void addDockableWindow(String name)
	{
		showDockableWindow(name);
	} //}}}

	//{{{ removeDockableWindow() method
	/**
	 * Removes the specified dockable window.
	 * @param name The dockable window name
	 * @since jEdit 2.6pre3
	 */
	public void removeDockableWindow(String name)
	{
		Entry entry = (Entry)windows.get(name);
		if(entry == null)
		{
			Log.log(Log.ERROR,this,"This DockableWindowManager"
				+ " does not have a window named " + name);
			return;
		}

		if(entry.win == null)
			return;

		if(entry.container instanceof FloatingWindowContainer)
		{
			entry.container.save(entry);
			entry.container.remove(entry);
			entry.container = null;
			entry.win = null;
		}
		else
			entry.container.show(null);
	} //}}}

	//{{{ toggleDockableWindow() method
	/**
	 * Toggles the visibility of the specified dockable window.
	 * @param name The dockable window name
	 */
	public void toggleDockableWindow(String name)
	{
		if(isDockableWindowVisible(name))
			removeDockableWindow(name);
		else
			addDockableWindow(name);
	} //}}}

	//{{{ getDockableWindow() method
	/**
	 * Returns the specified dockable window.
	 * @param name The name of the dockable window
	 * @since jEdit 4.1pre2
	 */
	public JComponent getDockableWindow(String name)
	{
		return getDockable(name);
	} //}}}

	//{{{ getDockable() method
	/**
	 * Returns the specified dockable window. For historical reasons, this
	 * does the same thing as <code>getDockableWindow()</code>.
	 * @param name The name of the dockable window
	 * @since jEdit 4.0pre1
	 */
	public JComponent getDockable(String name)
	{
		Entry entry = (Entry)windows.get(name);
		if(entry == null || entry.win == null)
			return null;
		else
			return entry.win;
	} //}}}

	//{{{ isDockableWindowVisible() method
	/**
	 * Returns if the specified dockable window is visible.
	 * @param name The dockable window name
	 */
	public boolean isDockableWindowVisible(String name)
	{
		Entry entry = (Entry)windows.get(name);
		if(entry == null || entry.win == null)
			return false;
		else
			return entry.container.isVisible(entry);
	} //}}}

	//{{{ isDockableWindowDocked() method
	/**
	 * Returns if the specified dockable window is docked into the
	 * view.
	 * @param name The dockable's name
	 * @since jEdit 4.0pre2
	 */
	public boolean isDockableWindowDocked(String name)
	{
		Entry entry = (Entry)windows.get(name);
		if(entry == null)
			return false;
		else
			return (entry.position != FLOATING);
	} //}}}

	//{{{ closeCurrentArea() method
	/**
	 * Closes the currently focused docking area.
	 * @since jEdit 4.1pre3
	 */
	public void closeCurrentArea()
	{
		Component comp = view.getFocusOwner();
		while(comp != null)
		{
			System.err.println(comp.getClass());
			if(comp instanceof PanelWindowContainer
				.DockablePanel)
			{
				PanelWindowContainer container =
					((PanelWindowContainer.DockablePanel)
					comp).getWindowContainer();
				container.show(null);
				return;
			}

			comp = comp.getParent();
		}

		getToolkit().beep();
	} //}}}

	//{{{ close() method
	/**
	 * Called when the view is being closed.
	 * @since jEdit 2.6pre3
	 */
	public void close()
	{
		if(!view.isPlainView())
		{
			top.save();
			left.save();
			bottom.save();
			right.save();
		}

		Enumeration enum = windows.elements();
		while(enum.hasMoreElements())
		{
			Entry entry = (Entry)enum.nextElement();
			if(entry.win != null)
				entry.remove();
		}
	} //}}}

	//{{{ getTopDockingArea() method
	public PanelWindowContainer getTopDockingArea()
	{
		return top;
	} //}}}

	//{{{ getLeftDockingArea() method
	public PanelWindowContainer getLeftDockingArea()
	{
		return left;
	} //}}}

	//{{{ getBottomDockingArea() method
	public PanelWindowContainer getBottomDockingArea()
	{
		return bottom;
	} //}}}

	//{{{ getRightDockingArea() method
	public PanelWindowContainer getRightDockingArea()
	{
		return right;
	} //}}}

	//{{{ propertiesChanged() method
	/**
	 * Called by the view when properties change.
	 * @since jEdit 2.6pre3
	 */
	public void propertiesChanged()
	{
		alternateLayout = jEdit.getBooleanProperty("view.docking.alternateLayout");

		Enumeration enum = windows.elements();
		while(enum.hasMoreElements())
		{
			Entry entry = (Entry)enum.nextElement();
			String position = entry.position;
			String newPosition = jEdit.getProperty(entry.factory.name
				+ ".dock-position");
			if(newPosition != null /* ??? */
				&& !newPosition.equals(position))
			{
				entry.position = newPosition;
				if(entry.container != null)
				{
					entry.container.remove(entry);
					entry.container = null;
					entry.win = null;
				}

				if(newPosition.equals(FLOATING))
					/* do nothing */;
				else
				{
					if(newPosition.equals(TOP))
						entry.container = top;
					else if(newPosition.equals(LEFT))
						entry.container = left;
					else if(newPosition.equals(BOTTOM))
						entry.container = bottom;
					else if(newPosition.equals(RIGHT))
						entry.container = right;
					else
						throw new InternalError("Unknown position: " + newPosition);

					entry.container.register(entry);
				}
			}

			if(entry.container instanceof FloatingWindowContainer)
			{
				SwingUtilities.updateComponentTreeUI(((JFrame)entry.container)
					.getRootPane());
			}
		}
	} //}}}

	//{{{ Private members
	private View view;
	private Hashtable windows;
	private boolean alternateLayout;
	private PanelWindowContainer left;
	private PanelWindowContainer right;
	private PanelWindowContainer top;
	private PanelWindowContainer bottom;
	//}}}

	//}}}

	//{{{ DockableLayout class
	public class DockableLayout implements LayoutManager2
	{
		// for backwards compatibility with plugins that fiddle with
		// jEdit's UI layout
		static final String CENTER = BorderLayout.CENTER;

		public static final String TOP_TOOLBARS = "top-toolbars";
		public static final String BOTTOM_TOOLBARS = "bottom-toolbars";

		static final String TOP_BUTTONS = "top-buttons";
		static final String LEFT_BUTTONS = "left-buttons";
		static final String BOTTOM_BUTTONS = "bottom-buttons";
		static final String RIGHT_BUTTONS = "right-buttons";

		Component topToolbars, bottomToolbars;
		Component center;
		Component top, left, bottom, right;
		Component topButtons, leftButtons, bottomButtons, rightButtons;

		//{{{ addLayoutComponent() method
		public void addLayoutComponent(String name, Component comp)
		{
			addLayoutComponent(comp,name);
		} //}}}

		//{{{ addLayoutComponent() method
		public void addLayoutComponent(Component comp, Object cons)
		{
			if(cons == null || CENTER.equals(cons))
				center = comp;
			else if(TOP_TOOLBARS.equals(cons))
				topToolbars = comp;
			else if(BOTTOM_TOOLBARS.equals(cons))
				bottomToolbars = comp;
			else if(TOP.equals(cons))
				top = comp;
			else if(LEFT.equals(cons))
				left = comp;
			else if(BOTTOM.equals(cons))
				bottom = comp;
			else if(RIGHT.equals(cons))
				right = comp;
			else if(TOP_BUTTONS.equals(cons))
				topButtons = comp;
			else if(LEFT_BUTTONS.equals(cons))
				leftButtons = comp;
			else if(BOTTOM_BUTTONS.equals(cons))
				bottomButtons = comp;
			else if(RIGHT_BUTTONS.equals(cons))
				rightButtons = comp;
		} //}}}

		//{{{ removeLayoutComponent() method
		public void removeLayoutComponent(Component comp)
		{
			if(center == comp)
				center = null;
			if(comp == topToolbars)
				topToolbars = null;
			if(comp == bottomToolbars)
				bottomToolbars = null;
			{
				// none of the others are ever meant to be
				// removed. retarded, eh? this needs to be
				// fixed eventually, for plugins might
				// want to do weird stuff to jEdit's UI
			}
		} //}}}

		//{{{ preferredLayoutSize() method
		public Dimension preferredLayoutSize(Container parent)
		{
			Dimension prefSize = new Dimension(0,0);
			Dimension _top = top.getPreferredSize();
			Dimension _left = left.getPreferredSize();
			Dimension _bottom = bottom.getPreferredSize();
			Dimension _right = right.getPreferredSize();
			Dimension _topButtons = topButtons.getPreferredSize();
			Dimension _leftButtons = leftButtons.getPreferredSize();
			Dimension _bottomButtons = bottomButtons.getPreferredSize();
			Dimension _rightButtons = rightButtons.getPreferredSize();
			Dimension _center = (center == null
				? new Dimension(0,0)
				: center.getPreferredSize());
			Dimension _topToolbars = (topToolbars == null
				? new Dimension(0,0)
				: topToolbars.getPreferredSize());
			Dimension _bottomToolbars = (bottomToolbars == null
				? new Dimension(0,0)
				: bottomToolbars.getPreferredSize());

			prefSize.height = _top.height + _bottom.height + _center.height
				+ _topButtons.height + _bottomButtons.height
				+ _topToolbars.height + _bottomToolbars.height;
			prefSize.width = _left.width + _right.width
				+ Math.max(_center.width,
				Math.max(_topToolbars.width,_bottomToolbars.width))
				+ _leftButtons.width + _rightButtons.width;

			return prefSize;
		} //}}}

		//{{{ minimumLayoutSize() method
		public Dimension minimumLayoutSize(Container parent)
		{
			// I'm lazy
			return preferredLayoutSize(parent);
		} //}}}

		//{{{ maximumLayoutSize() method
		public Dimension maximumLayoutSize(Container parent)
		{
			return new Dimension(Integer.MAX_VALUE,Integer.MAX_VALUE);
		} //}}}

		//{{{ layoutContainer() method
		public void layoutContainer(Container parent)
		{
			Dimension size = parent.getSize();

			Dimension _topButtons = topButtons.getPreferredSize();
			Dimension _leftButtons = leftButtons.getPreferredSize();
			Dimension _bottomButtons = bottomButtons.getPreferredSize();
			Dimension _rightButtons = rightButtons.getPreferredSize();
			Dimension _center = (center == null
				? new Dimension(0,0)
				: center.getPreferredSize());
			Dimension _topToolbars = (topToolbars == null
				? new Dimension(0,0)
				: topToolbars.getPreferredSize());
			Dimension _bottomToolbars = (bottomToolbars == null
				? new Dimension(0,0)
				: bottomToolbars.getPreferredSize());

			int _width = size.width - _leftButtons.width - _rightButtons.width;
			int _height = size.height - _topButtons.height - _bottomButtons.height;

			Dimension _top = top.getPreferredSize();
			Dimension _left = left.getPreferredSize();
			Dimension _bottom = bottom.getPreferredSize();
			Dimension _right = right.getPreferredSize();

			int topHeight = Math.min(Math.max(0,_height - _bottom.height),_top.height);
			int leftWidth = Math.min(Math.max(0,_width - _right.width),_left.width);
			int bottomHeight = Math.min(Math.max(0,_height - topHeight),_bottom.height);
			int rightWidth = Math.min(Math.max(0,_width - leftWidth),_right.width);

			DockableWindowManager.this.top.setDimension(topHeight);
			DockableWindowManager.this.left.setDimension(leftWidth);
			DockableWindowManager.this.bottom.setDimension(bottomHeight);
			DockableWindowManager.this.right.setDimension(rightWidth);

			if(alternateLayout)
			{
				topButtons.setBounds(
					_leftButtons.width,
					0,
					_width,
					_topButtons.height);

				leftButtons.setBounds(
					0,
					_topButtons.height + _top.height,
					_leftButtons.width,
					_height - _top.height - _bottom.height);

				bottomButtons.setBounds(
					_leftButtons.width,
					size.height - _bottomButtons.height,
					_width,
					_bottomButtons.height);

				rightButtons.setBounds(
					size.width - _rightButtons.width,
					_topButtons.height + _top.height,
					_rightButtons.width,
					_height - _top.height - _bottom.height);

				top.setBounds(
					_leftButtons.width,
					_topButtons.height,
					_width,
					topHeight);

				bottom.setBounds(
					_leftButtons.width,
					size.height - bottomHeight - _bottomButtons.height,
					_width,
					bottomHeight);

				left.setBounds(
					_leftButtons.width,
					_topButtons.height + topHeight,
					leftWidth,
					_height - topHeight - bottomHeight);

				right.setBounds(
					size.width - rightWidth - _rightButtons.width,
					_topButtons.height + topHeight,
					rightWidth,
					_height - topHeight - bottomHeight);
			}
			else
			{
				topButtons.setBounds(
					_leftButtons.width + leftWidth,
					0,
					_width - leftWidth - rightWidth,
					_topButtons.height);

				leftButtons.setBounds(
					0,
					_topButtons.height,
					_leftButtons.width,
					_height);

				bottomButtons.setBounds(
					_leftButtons.width + leftWidth,
					size.height - _bottomButtons.height,
					_width - leftWidth - rightWidth,
					_bottomButtons.height);

				rightButtons.setBounds(
					size.width - _rightButtons.width,
					_topButtons.height,
					_rightButtons.width,
					_height);

				top.setBounds(
					_leftButtons.width + leftWidth,
					_topButtons.height,
					_width - leftWidth - rightWidth,
					topHeight);
				bottom.setBounds(
					_leftButtons.width + leftWidth,
					size.height - bottomHeight - _bottomButtons.height,
					_width - leftWidth - rightWidth,
					bottomHeight);

				left.setBounds(
					_leftButtons.width,
					_topButtons.height,
					leftWidth,
					_height);

				right.setBounds(
					size.width - rightWidth - _rightButtons.width,
					_topButtons.height,
					rightWidth,
					_height);
			}

			if(topToolbars != null)
			{
				topToolbars.setBounds(
					_leftButtons.width + _left.width,
					_topButtons.height + _top.height,
					_width - _left.width - _right.width,
					_topToolbars.height);
			}

			if(bottomToolbars != null)
			{
				bottomToolbars.setBounds(
					_leftButtons.width + _left.width,
					_height - _bottom.height
					- _bottomToolbars.height
					+ _topButtons.height,
					_width - _left.width - _right.width,
					_bottomToolbars.height);
			}

			if(center != null)
			{
				center.setBounds(
					_leftButtons.width + _left.width,
					_topButtons.height + _top.height
					+ _topToolbars.height,
					_width - _left.width - _right.width,
					_height - _top.height - _bottom.height
					- _topToolbars.height
					- _bottomToolbars.height);
			}
		} //}}}

		//{{{ getLayoutAlignmentX() method
		public float getLayoutAlignmentX(Container target)
		{
			return 0.5f;
		} //}}}

		//{{{ getLayoutAlignmentY() method
		public float getLayoutAlignmentY(Container target)
		{
			return 0.5f;
		} //}}}

		//{{{ invalidateLayout() method
		public void invalidateLayout(Container target) {}
		//}}}
	} //}}}

	//{{{ Entry class
	class Entry
	{
		Factory factory;
		String title;
		String position;
		DockableWindowContainer container;

		// only set if open
		JComponent win;

		//{{{ Entry constructor
		Entry(Factory factory)
		{
			this(factory,jEdit.getProperty(factory.name
				+ ".dock-position",FLOATING));
		} //}}}

		//{{{ Entry constructor
		Entry(Factory factory, String position)
		{
			this.factory = factory;
			this.position = position;

			// get the title here, not in the factory constructor,
			// since the factory might be created before a plugin's
			// props are loaded
			title = jEdit.getProperty(factory.name + ".title");
			if(title == null)
				title = "NO TITLE PROPERTY: " + factory.name;

			if(position == null)
				position = FLOATING;
			else if(position.equals(FLOATING))
				/* do nothing */;
			else
			{
				if(position.equals(TOP))
					container = top;
				else if(position.equals(LEFT))
					container = left;
				else if(position.equals(BOTTOM))
					container = bottom;
				else if(position.equals(RIGHT))
					container = right;
				else
					throw new InternalError("Unknown position: " + position);

				container.register(this);
			}
		} //}}}

		//{{{ open() method
		void open()
		{
			win = factory.createDockableWindow(view,position);
			if(win == null)
			{
				// error occurred
				return;
			}

			Log.log(Log.DEBUG,this,"Adding " + factory.name + " with position " + position);

			if(position.equals(FLOATING))
			{
				container = new FloatingWindowContainer(
					DockableWindowManager.this);
				container.register(this);
			}

			container.add(this);
		} //}}}

		//{{{ remove() method
		void remove()
		{
			Log.log(Log.DEBUG,this,"Removing " + factory.name + " from "
				+ container);

			container.save(this);
			container.remove(this);

			if(container instanceof FloatingWindowContainer)
				container = null;

			win = null;
		} //}}}
	} //}}}
}
