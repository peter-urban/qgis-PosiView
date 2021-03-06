:orphan:

=====================================
Configuring a vehicle/object in depth
=====================================

**Configuration dialog**

  Go to the Mobiles/Vehicles tab.

  .. image:: _static/config_vehicles.png
      :align: center

  .. index:: Vehicles; in depth

  #. Create a new vehicle  by clicking on the ``+``-Button.
  #. Assign a unique name.
  #. Select an appearance that can be BOX, CROSS, X or a shape.
  #. If shape is used, select the outline as python array of points in the form ((x1, y1), (x2, y2), ..., (xn, yn)).
     Right mouse click offers some predefined shapes. The size of the shape should be normalized to (1, 1). A heading of zero points upward.
  #. Enter the real world size of the vehicle.
  #. If the position reference point is not the center (0, 0) of the shape, enter the offsets towards bow and starboard.
  #. The Z-Value defines the painting order on the canvas. Vehicles with higher values will be painted on top.
  #. Select colors for outline and fill brush. Transparency can be applied.
  #. Select the timeout for incoming position messages. 
     The corresponding panel in the tracking dock will switch to red if a timeout occures.
     A notification message is triggered if notification timeout is set.
  #. Select the timeout behavior. If checked, the vehicle will be faded out if a timeout occures.
  #. Choose color and length of the track.
  #. Select wether the vehicle should be labeled.
  #. Choose a provider from the list. If a provider supplies multiple position messages like USBL systems do, enter a filter.
     This could be the beacon id (USBL) or the MMSI (AIS) depending on the applied parser. Update the list.
  #. Click  ``Apply Properties``
