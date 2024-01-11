from typing import List
import re

from ..settings import Keyword, Sign
from .node import Node

class Parser(Node):
    ccode: str
    comment: str = None
    formating: str = None
    parsed: List[str]     # list of parsed directives or node parts
    
    def __init__(self, *args, **kwargs):
        self.parsed = []
        kwargs['ccode'] = kwargs['code']
        super().__init__(*args, **kwargs)
    
    def _strip(self, text):
        self.ccode = self.ccode[len(text):]

    def is_empty(self):
        return self.ccode.strip()==''

    def is_parsed(self, name:str):
        """ Check if directive or node part was already parsed

        :param str name: Name of a directive or node part
        """
        return name in self.parsed
    
    #####################
    # Directive keywords
    #####################
    
    def kwd_case(self):
        m=re.match(
            r'^(([a-zA-Z0-9_.-]*'+
            re.escape(Sign.CONDITION) + Keyword.CASE +
            r')\s+)',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_case')
            self.name = m.group(2)
            self._strip(m.group(1))
        else:
            m=re.match(
                r'^([a-zA-Z0-9_.-]*('+
                re.escape(Sign.CONDITION) + Keyword.ELSE +'|'+
                re.escape(Sign.CONDITION) + Keyword.END +'))',
                self.ccode
            )
            if m:
                self.parsed.append('kwd_case')
                self.name = m.group(1)
                self._strip(m.group(1))

    def kwd_unit(self):
        m=re.match(
            r'^(([a-zA-Z0-9_.-]*'+
            re.escape(Sign.VARIABLE) + Keyword.UNIT +
            r')\s+([^#]*))',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_unit')
            self.name = m.group(2)
            self.value_raw = m.group(3)
            self._strip(m.group(1))

    def kwd_source(self):
        m=re.match(
            r'^(([a-zA-Z0-9_.-]*'+
            re.escape(Sign.VARIABLE) + Keyword.SOURCE +
            r')\s+([^#]*))',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_source')
            self.name = m.group(2)
            self.value_raw = m.group(3)
            self._strip(m.group(1))

    def kwd_options(self):
        m=re.match(
            r'^(('+re.escape(Sign.VALIDATION)+Keyword.OPTIONS+r')\s+)',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_options')
            self.dimension = [(None,None)]
            self._strip(m.group(1))

    def kwd_constant(self):
        m=re.match(
            r'^('+re.escape(Sign.VALIDATION)+Keyword.CONSTANT+r')',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_constant')
            self._strip(m.group(1))

    def kwd_format(self):
        m=re.match(
            r'^(('+re.escape(Sign.VALIDATION)+Keyword.FORMAT+r')\s*)',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_format')
            self._strip(m.group(1))
            
    def kwd_tags(self):
        m=re.match(
            r'^(('+re.escape(Sign.VALIDATION)+Keyword.TAGS+r')\s*)',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_tags')
            self._strip(m.group(1))

    def kwd_description(self):
        kwd1 = re.escape(Sign.VALIDATION)+Keyword.DESCRIPTION
        kwd2 = re.escape(Sign.VALIDATION)+Keyword.DESCRIPTION[:4]
        m=re.match(
            r'^(('+kwd1+r'|'+kwd2+r')\s*)',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_description')
            self._strip(m.group(1))

    def kwd_condition(self):
        m=re.match(
            r'^(('+re.escape(Sign.VALIDATION)+Keyword.CONDITION+r')\s*)',
            self.ccode
        )
        if m:
            self.parsed.append('kwd_condition')
            self._strip(m.group(1))
            
    #############
    # Node parts
    #############
    
    def part_indent(self):
        m=re.match(r'^(\s*)',self.ccode)
        if m:
            self.parsed.append('part_indent')
            self.indent = len(m.group(1))
            self._strip(m.group(1))

    def part_name(self, path=True):
        if path is True:
            m=re.match(r'^([a-zA-Z0-9_.-]+)', self.ccode)  # format of node names
        else:
            m=re.match(r'^([a-zA-Z0-9_]+)', self.ccode)    # format of unit names
        if m:
            self.parsed.append('part_name')
            self.name = m.group(1)
            self._strip(m.group(1))
            if not self.is_empty() and self.ccode[0]!=' ':
                raise Exception("Name has an invalid format: "+self.code)
        else:
            raise Exception("Name has an invalid format: "+self.ccode)
        
    def part_type(self):
        types = [
            ('bool',    r'^(\s+bool)',                False, False),
            ('str',     r'^(\s+str)',                 False, False),
            ('table',   r'^(\s+table)',               False, False),
            ('int',     r'^(\s+(u|)int(16|32|64|))',  True,  True),
            ('float',   r'^(\s+float(32|64|128|))',   True,  False),
        ]
        for keyword, pattern, precision, unsigned in types:
            m=re.match(pattern, self.ccode)
            if m:
                self.parsed.append('part_type')
                self.keyword = keyword
                if unsigned and precision:   # integer
                    self.dtype_prop.append(m.group(2))
                    self.dtype_prop.append(m.group(3))
                elif precision:              # float
                    self.dtype_prop.append(m.group(2))
                self._strip(m.group(1))
                break
        if self.keyword is None:
            raise Exception(f"Type not recognized: {self.code}")

    def _part_dimension(self):
        pattern = r'^(\[([0-9:,]+)\])'
        m=re.match(pattern, self.ccode)
        if m:
            dims = m.group(2).split(',')
            var = []
            for dim in dims:
                if ":" in dim:
                    dmin,dmax = dim.split(':')
                    var.append((
                        int(dmin) if dmin else None,
                        int(dmax) if dmax else None
                    ))
                else:
                    var.append((int(dim), int(dim)))
            self._strip(m.group(1))
            return var
        return None
        
    def part_dimension(self):
        if dim := self._part_dimension():
            self.parsed.append('part_dimension')
            self.dimension = dim
                        
    def part_equal(self):
        m=re.match(r'^(\s*=\s*)', self.ccode)
        if m:
            self.parsed.append('part_equal')
            self._strip(m.group(1))
            
    def part_value(self):
        # Parse reference
        self.part_reference(inject=True)
        if self.is_parsed('part_reference'):
            self.parsed.append('part_value')
            return
        # Parse function
        self.part_function()
        if self.is_parsed('part_function'):
            self.parsed.append('part_value')
            return
        # Parse expression
        self.part_expression()
        if self.is_parsed('part_expression'):
            self.parsed.append('part_value')
            return
        # If not block value, parse standard text value
        m=re.match(r'^(("""(.*)"""|"(.*)"|\'(.*)\'|([^# ]+)))', self.ccode)
        if m:
            self.parsed.append('part_value')
            # Reduce matches
            results = [x for x in m.groups()[1:] if x is not None]
            # Save value
            self.value_raw = results[1]
            self._strip(m.group(1))
        if self.value_raw is None:
            raise Exception("Value cannot start with an empty string:", self.code)
        
    def part_reference(self, inject=False):
        m=re.match(r'^(\s*({([^}]*)}))', self.ccode)
        if m:
            self.parsed.append('part_reference')
            self.value_ref = m.group(3)
            self.value_raw = '' 
            if not inject:
                if self.name:
                    self.name = f"{self.name}.{m.group(2)}"
                else:
                    self.name = f"{m.group(1)}"
            self._strip(m.group(1))
            self.part_slice()

    def part_slice(self):
        if dim := self._part_dimension():
            self.parsed.append('part_slice')
            self.value_slice = dim

    def part_format(self):  # template reference text format
        m=re.match(r'^(:[0-9.]*[sdfeb]+)', self.ccode)
        if m:
            self.parsed.append('part_format')
            self.formating = m.group(1)
            self._strip(m.group(1))

    def part_function(self):
        m=re.match(r'^(\(([a-zA-Z0-9_-]*)\))', self.ccode)
        if m:
            self.parsed.append('part_function')
            # Reduce matches
            self.value_raw = ''
            self.value_fn = m.group(2)
            self._strip(m.group(1))
            
    def part_expression(self):
        m=re.match(r'^(\(("""(.*)"""|"(.*)"|\'(.*)\')\))', self.ccode)
        if m:
            self.parsed.append('part_expression')
            # Reduce matches
            results = [x for x in m.groups()[1:] if x is not None]
            self.value_raw = ''
            self.value_expr = results[1]
            self._strip(m.group(1))
                    
    def part_units(self):
        # In numerical expressions following starting
        # signs +-*/ have to be explicitely excluded
        n=re.match(r'^\s+[\/*+-]+', self.ccode)
        m=re.match(r'^(\s+([^\s#=]+))', self.ccode)
        if m and not n:
            self.parsed.append('part_units')
            self.units_raw = m.group(2)
            self._strip(m.group(1))
        
    def part_comment(self):
        m=re.match(r'^(\s*#\s*(.*))$', self.ccode)
        if m:
            self.parsed.append('part_comment')
            self.comment = m.group(2)
            self._strip(m.group(1))
