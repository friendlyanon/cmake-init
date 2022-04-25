<?xml version="1.0" encoding="utf-8"?>
<x:stylesheet xmlns:x="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <x:output method="xml" version="1.0" encoding="utf-8" indent="yes" />
  <x:template name="trim">
    <x:param name="str" />
    <x:choose>
      <x:when test="string-length($str) &gt; 0 and substring($str, 1, 1) = ' '">
        <x:call-template name="trim">
          <x:with-param name="str">
            <x:value-of select="substring($str, 2)" />
          </x:with-param>
        </x:call-template>
      </x:when>
      <x:when test="string-length($str) &gt; 0 and substring($str, string-length($str)) = ' '">
        <x:call-template name="trim">
          <x:with-param name="str">
            <x:value-of select="substring($str, 1, string-length($str) - 1)" />
          </x:with-param>
        </x:call-template>
      </x:when>
      <x:otherwise>
        <x:value-of select="$str" />
      </x:otherwise>
    </x:choose>
  </x:template>
  <x:template name="unixtime-to-datetime">
    <x:param name="unixTime" />

    <x:variable name="JDN" select="floor($unixTime div 86400) + 2440588" />
    <x:variable name="secs" select="$unixTime mod 86400" />   

    <x:variable name="f" select="$JDN + 1401 + floor((floor((4 * $JDN + 274277) div 146097) * 3) div 4) - 38" />
    <x:variable name="e" select="4 * $f + 3" />
    <x:variable name="g" select="floor(($e mod 1461) div 4)" />
    <x:variable name="h" select="5 * $g + 2" />

    <x:variable name="d" select="floor(($h mod 153) div 5 ) + 1" />
    <x:variable name="m" select="(floor($h div 153) + 2) mod 12 + 1" />
    <x:variable name="y" select="floor($e div 1461) - 4716 + floor((14 - $m) div 12)" />

    <x:variable name="H" select="floor($secs div 3600)" />
    <x:variable name="M" select="floor($secs mod 3600 div 60)" />
    <x:variable name="S" select="$secs mod 60" />

    <x:value-of select="$y" />
    <x:text>-</x:text>
    <x:value-of select="format-number($m, '00')" />
    <x:text>-</x:text>
    <x:value-of select="format-number($d, '00')" />
    <x:text>T</x:text>
    <x:value-of select="format-number($H, '00')" />
    <x:text>:</x:text>
    <x:value-of select="format-number($M, '00')" />
    <x:text>:</x:text>
    <x:value-of select="format-number($S, '00')" />
  </x:template> 
  <x:template match="/Site">
    <x:variable name="OSRelease">
      <x:call-template name="trim">
        <x:with-param name="str" select="@OSRelease" />
      </x:call-template>
    </x:variable>
    <x:variable name="OSVersion">
      <x:call-template name="trim">
        <x:with-param name="str" select="@OSVersion" />
      </x:call-template>
    </x:variable>
    <testsuites
      failures="{count(Testing/Test[@Status = 'failed'])}"
      skipped="{count(Testing/Test[@Status = 'notrun'])}"
      tests="{count(Testing/Test)}">

      <testsuite
        failures="{count(Testing/Test[@Status = 'failed'])}"
        skipped="{count(Testing/Test[@Status = 'notrun'])}"
        tests="{count(Testing/Test)}"
        time="{Testing/ElapsedMinutes}"
        name="{@BuildName}"
        hostname="{@Name}">

        <x:attribute name="timestamp">
          <x:call-template name="unixtime-to-datetime">
            <x:with-param name="unixTime" select="Testing/StartTestTime" />
          </x:call-template>
        </x:attribute>

        <x:comment>
          <x:text>&#x20;Start test time:&#x20;</x:text>
          <x:value-of select="Testing/StartTestTime" />
          <x:text>&#x20;</x:text>
        </x:comment>

        <properties>
          <property name="BuildName" value="{@BuildName}" />
          <property name="BuildStamp" value="{@BuildStamp}" />
          <property name="Name" value="{@Name}" />
          <property name="Generator" value="{@Generator}" />
          <property name="CompilerName" value="{@CompilerName}" />
          <property name="OSName" value="{@OSName}" />
          <property name="Hostname" value="{@Hostname}" />
          <property name="OSRelease" value="{$OSRelease}" />
          <property name="OSVersion" value="{$OSVersion}" />
          <property name="OSPlatform" value="{@OSPlatform}" />
          <property name="Is64Bits" value="{@Is64Bits}" />
          <property name="VendorString" value="{@VendorString}" />
          <property name="VendorID" value="{@VendorID}" />
          <property name="FamilyID" value="{@FamilyID}" />
          <property name="ModelID" value="{@ModelID}" />
          <property name="ProcessorCacheSize" value="{@ProcessorCacheSize}" />
          <property name="NumberOfLogicalCPU" value="{@NumberOfLogicalCPU}" />
          <property name="NumberOfPhysicalCPU" value="{@NumberOfPhysicalCPU}" />
          <property name="TotalVirtualMemory" value="{@TotalVirtualMemory}" />
          <property name="TotalPhysicalMemory" value="{@TotalPhysicalMemory}" />
          <property name="LogicalProcessorsPerPhysical" value="{@LogicalProcessorsPerPhysical}" />
          <property name="ProcessorClockFrequency" value="{@ProcessorClockFrequency}" />
        </properties>

        <x:comment>
          <x:text>&#x20;'classname' refers to the directory where the test was defined&#x20;</x:text>
        </x:comment>

        <x:apply-templates select="Testing/Test" />
      </testsuite>
    </testsuites>
  </x:template>
  <x:template match="Testing/Test">
    <x:variable name="time">
      <x:choose>
        <x:when test="@Status = 'notrun'">0</x:when>
        <x:otherwise>
          <x:value-of select="Results/NamedMeasurement[@name = 'Execution Time']/Value" />
        </x:otherwise>
      </x:choose>
    </x:variable>

    <x:element name="testcase">

      <x:attribute name="name">
        <x:value-of select="Name" />
      </x:attribute>
      <x:attribute name="classname">
        <x:value-of select="substring(Path, 3)" />
      </x:attribute>
      <x:attribute name="status">
        <x:value-of select="@Status" />
      </x:attribute>

      <x:if test="@Status != 'notrun'">
        <x:attribute name="time">
          <x:value-of select="Results/NamedMeasurement[@name = 'Execution Time']/Value" />
        </x:attribute>

        <x:comment>
          <x:text>&#x20;Processors:&#x20;</x:text>
          <x:value-of select="Results/NamedMeasurement[@name = 'Processors']/Value" />
          <x:text>&#x20;</x:text>
        </x:comment>
        <x:comment>
          <x:text>&#x20;Completion Status:&#x20;</x:text>
          <x:value-of select="Results/NamedMeasurement[@name = 'Completion Status']/Value" />
          <x:text>&#x20;</x:text>
        </x:comment>
      </x:if>

      <x:choose>
        <x:when test="@Status = 'passed'">
          <x:apply-templates select="Results/Measurement/Value" />
        </x:when>
        <x:when test="@Status = 'failed'">
          <x:variable name="failtype">
            <x:value-of select="Results/NamedMeasurement[@name = 'Exit Code']/Value" />
          </x:variable>
          <x:variable name="failcode">
            <x:value-of select="Results/NamedMeasurement[@name = 'Exit Value']/Value" />
          </x:variable>
          <failure message="{$failtype} ({$failcode})" />
          <x:apply-templates select="Results/Measurement/Value" />
        </x:when>
        <x:when test="@Status = 'notrun'">
          <skipped />
        </x:when>
      </x:choose>

    </x:element>
  </x:template>
  <x:template match="Results/Measurement/Value">
    <x:if test=". != ''">
      <system-out>
        <x:value-of select="." />
      </system-out>
    </x:if>
  </x:template>
</x:stylesheet>
