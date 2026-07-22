import React from 'react';
import { IoSend, IoWater } from "react-icons/io5";
import { FaWater, FaMapMarkerAlt, FaCalendarAlt, FaChartLine, FaGlobe } from "react-icons/fa";
import { MdScience } from "react-icons/md";
import { TbTemperature, TbDroplet, TbRuler } from "react-icons/tb";

// Test component to verify all icons load correctly
const IconTest = () => {
  return (
    <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', padding: '20px' }}>
      <IoSend title="IoSend" />
      <IoWater title="IoWater" />
      <FaWater title="FaWater" />
      <FaMapMarkerAlt title="FaMapMarkerAlt" />
      <FaCalendarAlt title="FaCalendarAlt" />
      <FaChartLine title="FaChartLine" />
      <FaGlobe title="FaGlobe" />
      <MdScience title="MdScience" />
      <TbTemperature title="TbTemperature" />
      <TbDroplet title="TbDroplet" />
      <TbRuler title="TbRuler" />
    </div>
  );
};

export default IconTest;